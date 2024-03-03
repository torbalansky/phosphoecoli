from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import PhosphoProtein, PhosphoSite
from django.contrib import messages
from .forms import SignUpForm, ContactForm, ProteinSearchForm
from .models import Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly.graph_objects as go
import plotly.offline as py

def home(request):
    return render(request, 'home.html', {})

# Login view function
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            messages.success(request, "You are logged in.")
            return redirect('home')
        else:
            messages.error(request, "Ups, something went wrong. Please try again.")
            return render(request, "login.html", {})
    else:
        return render(request, "login.html", {})

# Logout view function
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

# Register view function
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() 
            institution_name = form.cleaned_data['institution_name']
            country = form.cleaned_data['country']
            profile = Profile.objects.create(user=user, institution_name=institution_name, country=country)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
    else:
        form = SignUpForm() 
        return render(request, "register.html", {'form': form})
    
    return render(request, "register.html", {'form': form})

# Contact view function
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            html = render_to_string('contact_form.html', {
                'name': name,
                'email': email,
                'content': content
            })

            send_mail('The contact form subject', 'This is the message', 'torbalansky@gmail.com', ['torbalansky@gmail.com'], html_message=html)
            messages.success(request, "Message sent. I will get back to you as soon as possible.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form
    })

# Proteins list view class
class ProteinsListView(ListView):
    model = PhosphoProtein # Define model
    template_name = "protein_list.html" # Define template name
    context_object_name = "proteins" # Define context object name
    
    def get_queryset(self): # Override queryset method
        queryset = super().get_queryset()
        uniprot_code = self.request.GET.get("uniprot_code")
        gene_name = self.request.GET.get("gene_name")
        protein_name = self.request.GET.get("protein_name")
        modification_type = self.request.GET.get("modification_type")

        # Initialize combined query
        combined_query = Q()

        if uniprot_code:
            combined_query |= Q(uniprot_code__icontains=uniprot_code)
        if gene_name:
            combined_query |= Q(gene_name__icontains=gene_name)
        if protein_name:
            combined_query |= Q(protein_name__icontains=protein_name)
        if modification_type and modification_type != '': 
            combined_query |= Q(phosphosite__modification_type__iexact=modification_type)

        return queryset.filter(combined_query).distinct() # Filter queryset and return

    def get_context_data(self, **kwargs): # Override get_context_data method
        context = super().get_context_data(**kwargs)
        context["form"] = ProteinSearchForm(self.request.GET)
        if not context["proteins"]:
            error_message = "There is no data available."
            messages.error(self.request, error_message)
            context["error_message"] = error_message

        phosphosites_dict = {}  # Initialize dictionary to store phosphosites
        for protein in context["proteins"]:
            phosphosites = list(PhosphoSite.objects.filter(protein=protein))
            phosphosites.sort(key=lambda x: x.modification_type)
            phosphosites_dict[protein.pk] = phosphosites 

            context["phosphosites_dict"] = phosphosites_dict # Add phosphosites dictionary to context

        return context
    

class ProteinDetailView(DetailView):
    model = PhosphoProtein
    template_name = "protein_details.html"
    context_object_name = "protein"

    def phospho_chart_image(self):
        protein = self.get_object()
        sequence = protein.sequence
        phosphosites = PhosphoSite.objects.filter(protein=protein)

        # Create a scatter plot
        fig = go.Figure(layout=dict(height=400, width=1000))
        fig.add_trace(go.Scatter(x=list(range(1, len(sequence) + 1)), y=[0] * len(sequence),
        mode='text', text=list(sequence), textposition="top center", showlegend=False))

        # Add phosphosites as points
        for phosphosite in phosphosites:
            hover_text = f"Phosphosite - {phosphosite.modification_type}{phosphosite.position}<br>Window -/+ 5aa: {phosphosite.window_5_aa}"
            fig.add_trace(go.Scatter(x=[phosphosite.position], y=[0.5], mode='markers', 
            marker=dict(size=10, color='blue'), name=f'Phosphosite - {phosphosite.modification_type}{phosphosite.position}', 
            hoverinfo='text', text=hover_text))
            fig.add_trace(go.Scatter(x=[phosphosite.position, phosphosite.position], y=[0.04, 0.5], mode='lines',
                                     line=dict(color='black', width=0.2), showlegend=False))
        # Update layout
        fig.update_layout(
            title=f'Phosphosites in {protein.gene_name}',
            xaxis_title='Residue Number', 
            yaxis_title='Phosphosites',
            xaxis=dict(tickmode='linear', range=[0, len(sequence)], dtick=50), 
            yaxis=dict(visible=False),
            clickmode='event+select'              
            )

        # Generate HTML representation of the chart
        chart_html = py.plot(fig, output_type='div')

        return chart_html


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chart_image'] = self.phospho_chart_image()
        protein = self.get_object() 
       
        context['pdb_code'] = protein.pdb_code if protein.pdb_code else None
        return context

# Overview view function
def overview(request):
    return render(request, 'overview.html')

# Resources view function
def resources(request):
    return render(request, 'resources.html')

# Cite view function
def cite(request):
    return render(request, 'cite.html')

# Guide view function
def guide(request):
    return render(request, 'guide.html')

# Search phosphoprotein view function
def search_phosphoprotein(request):
    if request.method == 'GET':
        uniprot_id = request.GET.get('Uniprot_Code')
        gene_name = request.GET.get('Gene_Name')
        protein_name = request.GET.get('Protein_Name')
        queryset = PhosphoProtein.objects.all() # Get all phosphoproteins

        if uniprot_id:
            queryset = queryset.filter(uniprot_code__icontains=uniprot_id)

        if gene_name:
            queryset = queryset.filter(gene_name__icontains=gene_name)

        if protein_name:
            queryset = queryset.filter(protein_name__icontains=protein_name)

        phospho_proteins = queryset # Assign filtered queryset to variable

        if not phospho_proteins:
            messages.error(request, "No data available.")

        return render(request, 'protein_list.html', {'phospho_proteins': phospho_proteins})

    return render(request, 'home.html')

# Export protein as PDF view function
def export_protein_as_pdf(request, pk):
    protein = get_object_or_404(PhosphoProtein, id=pk)

    template_path = 'pdf_template.html'

    context = {
        'protein': protein,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{protein.protein_name}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
