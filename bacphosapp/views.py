from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import PhosphoProtein
from django.contrib import messages
from .forms import SignUpForm, ContactForm, ProteinSearchForm, PhosphoProteinForm, UserUpdateForm
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
from django.template.defaulttags import register
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
import base64
import matplotlib
matplotlib.use('Agg')
import requests
import io
import numpy as np

def home(request):
    return render(request, 'home.html', {})

# Register view function
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            institution_name = form.cleaned_data['institution_name']
            country = form.cleaned_data['country']
            profile = Profile.objects.create(user=user, institution_name=institution_name, country=country)
            messages.success(request, "Your account has been created. It will be activated once approved by the admin.")
            return redirect('home')
    else:
        form = SignUpForm() 
    return render(request, "register.html", {'form': form})

# Login view function
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            profile = get_object_or_404(Profile, user=user)
            if profile.approved:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect('profile' , pk=user.pk)
            elif not user.is_active:
                messages.error(request, "Your account is inactive. Please contact the administrator.")
            elif not profile.approved:
                messages.error(request, "Your account is not yet approved by the administrator.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, "login.html", {})

# Logout view function
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

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

# Protein list view function
class ProteinsListView(ListView):
    model = PhosphoProtein
    template_name = "protein_list.html"
    context_object_name = "proteins"
    paginate_by = 10

    def get_queryset(self):
        # Get the initial queryset of all PhosphoProtein objects
        queryset = super().get_queryset()
        # Filter queryset to include only approved proteins
        queryset = queryset.filter(approved=True)

        # Get search parameters from the request
        search_category = self.request.GET.get("search_category")
        search_query = self.request.GET.get("q")
        modification_type = self.request.GET.get("modification_type")
        window_5_aa = self.request.GET.get("window_5_aa")
        coli_strain = self.request.GET.get("coli_strain")

        # Apply search filters if provided
        if search_query:
            if search_category == "uniprot":
                queryset = queryset.filter(uniprot_code__icontains=search_query)
            elif search_category == "gene":
                queryset = queryset.filter(gene_name__icontains=search_query)
            elif search_category == "protein":
                queryset = queryset.filter(protein_name__icontains=search_query)
            elif search_category == 'window':
                queryset = queryset.filter(window_5_aa__icontains=search_query)
            else:
                # If search_category is empty or "Any Field" is selected, search across all relevant fields
                queryset = queryset.filter(
                    Q(uniprot_code__icontains=search_query) |
                    Q(gene_name__icontains=search_query) |
                    Q(protein_name__icontains=search_query) |
                    Q(window_5_aa__icontains=search_query)
                )

        # Apply modification type filter if provided
        if modification_type:
            queryset = queryset.filter(modification_type=modification_type)
        
        # Apply coli strain filter if provided
        if coli_strain:
            queryset = queryset.filter(coli_strain=coli_strain)

        # Return distinct results
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        # Get the context data including pagination information
        context = super().get_context_data(**kwargs)
        # Pass search parameters to the template
        context['search_category'] = self.request.GET.get('search_category', '')
        context['q'] = self.request.GET.get('q', '')
        context['modification_type'] = self.request.GET.get('modification_type', '')
        context['peptide_sequence'] = self.request.GET.get('peptide_sequence', '')
        context['coli_strain'] = self.request.GET.get('coli_strain', '')
        return context
    
@register.filter
def add_position(sequence):
    return [(position + 1, aa) for position, aa in enumerate(sequence)]

def parse_iupred_response(text):
    # Split the response by lines
    lines = text.split('\n')

    # Initialize a list to store disordered regions
    disordered_regions = []

    # Iterate over each line in the response
    for line in lines:
        # Skip empty lines and lines starting with #
        if not line.strip() or line.startswith("#"):
            continue

        # Split the line by tabs
        parts = line.split()

        # Check if the line has enough parts and if the first part is a valid integer
        if len(parts) >= 3 and parts[0].isdigit():
            # Extract residue position, amino acid, and IUPred score
            position = int(parts[0])
            amino_acid = parts[1]
            iupred_score = float(parts[2])

            # Check if the residue is predicted to be disordered (IUPred score > 0.5)
            if iupred_score > 0.001:
                # Add the disordered region to the list
                disordered_regions.append({'position': position, 'amino_acid': amino_acid, 'iupred_score': iupred_score})

    return disordered_regions

# Protein detail view function
class ProteinDetailView(DetailView):
    model = PhosphoProtein
    template_name = "protein_details.html"
    context_object_name = "protein"

    def get_disordered_regions(self, uniprot_code):
        # Make a request to the IUPred2A API
        url = f"http://iupred3.elte.hu/iupred3/{uniprot_code}"
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the response to extract disordered regions
            disordered_regions = parse_iupred_response(response.text)
            return disordered_regions
        else:
            return None

    def phospho_chart_image(self):
        protein = self.get_object()
        sequence = protein.sequence

        # Sort phosphosites alphabetically or numerically
        phosphosite_positions = sorted(str(protein.position).split(',')) if protein.position else []

        # Fetch disordered regions for the protein
        disordered_regions = self.get_disordered_regions(protein.uniprot_code)

        # Get disorder propensity scores for all residues
        disorder_scores = np.zeros(len(sequence))

        if disordered_regions:
            for region in disordered_regions:
                start_pos = region['position']
                end_pos = start_pos + len(region['amino_acid']) - 1
                disorder_scores[start_pos - 1:end_pos] = region['iupred_score']

        # Create a scatter plot with disorder propensity overlay
        fig = go.Figure(layout=dict(height=400, width=1000))
        fig.add_trace(go.Scatter(x=list(range(1, len(sequence) + 1)), y=[0] * len(sequence),
                                mode='text', text=list(sequence), textposition="top center", showlegend=False))

        # Add disorder propensity curve
        fig.add_trace(go.Scatter(x=list(range(1, len(sequence) + 1)), y=disorder_scores,
                                mode='lines', line=dict(color='red', width=1), name='Disorder Propensity'))
       
        # Calculate the range around the leading phosphosite and update x-axis range for the disorder propensity curve
        leading_position = int(phosphosite_positions[0])
        start_range = max(leading_position - 50, 0)
        end_range = min(leading_position + 50, len(sequence))
        disorder_range_x = list(range(start_range, end_range + 1))
        disorder_range_y = disorder_scores[start_range - 1:end_range]

        # Add main phosphosite
        for position in phosphosite_positions:
            hover_text = f"Phosphosite - {protein.modification_type}{position}<br>Window -/+ 5aa: {protein.window_5_aa}"
            fig.add_trace(go.Scatter(x=[int(position)], y=[0.8], mode='markers',
                                    marker=dict(size=10, color='blue'), name=f'Phosphosite - {protein.modification_type}{position}',
                                    hoverinfo='text', text=hover_text))
            fig.add_trace(go.Scatter(x=[int(position), int(position)], y=[0.04, 0.8], mode='lines',
                                    line=dict(color='black', width=0.2), showlegend=False))

        # Add related phosphosites
        related_phosphosites = PhosphoProtein.objects.filter(gene_name=protein.gene_name, coli_strain=protein.coli_strain, uniprot_code=protein.uniprot_code).exclude(pk=protein.pk)
        for related_protein in related_phosphosites:
            related_positions = sorted(str(related_protein.position).split(',')) if related_protein.position else []
            for position in related_positions:
                hover_text = f"Phosphosite - {related_protein.modification_type}{position}<br>Window -/+ 5aa: {related_protein.window_5_aa}"
                fig.add_trace(go.Scatter(x=[int(position)], y=[0.8], mode='markers',
                                        marker=dict(size=10, color='black'), name=f'Phosphosite - {related_protein.modification_type}{position}',
                                        hoverinfo='text', text=hover_text))
                fig.add_trace(go.Scatter(x=[int(position), int(position)], y=[0.04, 0.8], mode='lines',
                                        line=dict(color='black', width=0.2), showlegend=False))

        # Add threshold line at y = 0.5
        fig.add_shape(type="line", x0=1, x1=len(sequence), y0=0.5, y1=0.5,
                line=dict(color="black", width=1, dash="dash"), name='Threshold')
        
        # Update layout
        fig.update_layout(
            title=f'Phosphosites & Disorder Propensity (IUPred3) - {protein.gene_name}',
            xaxis_title='Residue Number',
            yaxis_title='',
            yaxis=dict(
                range=[0, 1],
                tickvals=[0, 0.5, 1],
                ticktext=['0', '0.5', '1'],
                visible=True
            ),
            xaxis=dict(
                range=[start_range, end_range]
            ),
            clickmode='event+select',
            margin=dict(t=50),
        )

        # Generate HTML representation of the chart
        chart_html = py.plot(fig, output_type='div')

        return chart_html

    def disordered_chart_image(self):
        protein = self.get_object()
        uniprot_code = protein.uniprot_code

        # Fetch disordered regions for the protein
        disordered_regions = self.get_disordered_regions(uniprot_code)

        # Get disorder propensity scores for all residues
        disorder_scores = np.zeros(len(protein.sequence))

        if disordered_regions:
            for region in disordered_regions:
                start_pos = region['position']
                end_pos = start_pos + len(region['amino_acid']) - 1
                disorder_scores[start_pos - 1:end_pos] = region['iupred_score']

        # Create a curve plot for disorder propensity
        plt.figure(figsize=(10, 4))
        plt.plot(range(1, len(protein.sequence) + 1), disorder_scores, color='red', label='Disorder Propensity')
        plt.xlabel('Residue Number')
        plt.ylabel('Disorder Propensity')
        plt.title(f'Disorder Propensity Visualization ({protein.gene_name})')
        plt.xlim(1, len(protein.sequence))
        plt.ylim(0, 1)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.legend(loc='upper right')
        plt.tight_layout()

        # Convert the plot to a base64-encoded string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_image = buffer.getvalue()
        buffer.close()

        plot_base64 = base64.b64encode(plot_image).decode('utf-8')

        # Generate HTML representation of the plot
        chart_html = f'<img src="data:image/png;base64,{plot_base64}" />'

        plt.close()

        return chart_html

    def get_related_proteins(self):
        protein = self.get_object()
        related_proteins = PhosphoProtein.objects.filter(gene_name=protein.gene_name, coli_strain=protein.coli_strain, uniprot_code=protein.uniprot_code).exclude(pk=protein.pk)
        related_proteins = related_proteins.order_by('modification_type', 'position')
        return related_proteins

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chart_image'] = self.phospho_chart_image()
        context['disordered_chart_image'] = self.disordered_chart_image()
        protein = self.get_object()
        context['sequence_with_positions'] = add_position(protein.sequence) if protein.sequence else None
        context['pdb_code'] = protein.pdb_code
        uniprot_code = protein.uniprot_code
        # Fetch all PhosphoProtein instances with the same gene name
        related_proteins = PhosphoProtein.objects.filter(gene_name=protein.gene_name).exclude(pk=protein.pk)

        # Fetch related proteins ordered alphabetically
        related_proteins = self.get_related_proteins()

        # Extract related positions
        related_positions = [int(position) for related_protein in related_proteins for position in str(related_protein.position).split(',')]
        context['related_positions'] = related_positions

        # Pass related proteins to the template context
        context['related_proteins'] = related_proteins
        context['pdb_code'] = protein.pdb_code
        # Sort phosphosite positions alphabetically or numerically
        phosphosite_positions = sorted(str(protein.position).split(',')) if protein.position else []
        context['phosphosite_positions'] = phosphosite_positions
        pmids = [pmid.strip() for pmid in protein.reference.split(';') if pmid.strip()]
        context['pmids'] = pmids
        context['coli_strain'] = protein.coli_strain
        # Fetch disordered regions for the protein
        disordered_regions = self.get_disordered_regions(uniprot_code)
        # Pass disordered regions to the template context
        context['disordered_regions'] = disordered_regions
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

    # Fetch related proteins
    related_proteins = PhosphoProtein.objects.filter(gene_name=protein.gene_name).exclude(pk=protein.pk)
    related_proteins = related_proteins.order_by('modification_type', 'position')

    sequence_chunks = [protein.sequence[i:i+80] for i in range(0, len(protein.sequence), 60)]
    protein.sequence_chunks = sequence_chunks

    template_path = 'pdf_template.html'

    context = {
        'protein': protein,
        'related_proteins': related_proteins,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{protein.protein_name}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

# Update user view function
def update_user(request, pk):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        current_profile = Profile.objects.get(user=current_user)

        if request.method == "POST":
            user_form = UserUpdateForm(request.POST, instance=current_user)
            if user_form.is_valid():
                user_form.save()
                current_profile.institution_name = user_form.cleaned_data['institution_name']
                current_profile.country = user_form.cleaned_data['country']
                current_profile.save()

                login(request, current_user)
                messages.success(request, "Your profile has been updated.")
                return redirect('home')
            else:
                messages.error(request, "There was an error updating your profile. Please try again.")
        else:
            user_form = UserUpdateForm(instance=current_user)
            return render(request, "update_user.html", {'user_form': user_form })
    else:
        messages.success(request, "You have to be logged in.")
        return redirect('home')

# Delete user view function
def delete_user(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=pk)
        
        if request.user == user:
            user.delete()
            messages.success(request, "Your account has been successfully deleted.")
            return redirect('home')
        else:
            messages.error(request, "Something went wrong. Please try again.")
    else:
        messages.error(request, "You must be logged in to perform this task.")
    
    return redirect('home')

# Profile view function
def profile(request, pk):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user_id=pk)
            user = profile.user

            # Fetch existing phosphoproteins
            user_phosphoproteins = PhosphoProtein.objects.filter(submitted_by=user)

            if request.method == 'POST':
                phosphoprotein_form = PhosphoProteinForm(request.POST)
                if phosphoprotein_form.is_valid():
                    phosphoprotein = phosphoprotein_form.save(commit=False)
                    phosphoprotein.submitted_by = request.user
                    phosphoprotein.approved = False  # Mark as unapproved for all users
                    phosphoprotein.save()
                    messages.success(request, "Phosphoprotein submitted successfully. It will be visible after approval.")
                    return HttpResponseRedirect(request.path_info)  # Redirect to the same page to avoid resubmission
                else:
                    messages.error(request, "Phosphoprotein form validation failed.")
            else:
                phosphoprotein_form = PhosphoProteinForm()

            # Fetch only approved phosphoproteins for display
            approved_phosphoproteins = PhosphoProtein.objects.filter(
                Q(submitted_by=user) | Q(approved=True)
            )

            context = {
                "profile": profile,
                "user_phosphoproteins": user_phosphoproteins,
                "approved_phosphoproteins": approved_phosphoproteins,
                "phosphoprotein_form": phosphoprotein_form,
            }
            return render(request, "profile.html", context)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")
    else:
        messages.error(request, "You must be logged in to access this!")
        return redirect('login')

@login_required
def update_phosphoprotein(request, user_id, pk):
    # Fetch the phosphoprotein instance to update
    phosphoprotein = get_object_or_404(PhosphoProtein, pk=pk)

    if request.method == 'POST':
        # Populate the form with the instance data
        form = PhosphoProteinForm(request.POST, instance=phosphoprotein)
        if form.is_valid():
            phosphoprotein = form.save(commit=False)
            phosphoprotein.submitted_by = request.user
            phosphoprotein.save()
            messages.success(request, "Phosphoprotein updated successfully.")
            return redirect('profile', pk=user_id)
        else:
            messages.error(request, "Form validation failed.")
    else:
        # Populate the form with the instance data
        form = PhosphoProteinForm(instance=phosphoprotein)

    return render(request, 'update_phosphoprotein.html', {'form': form})

# Delete phosphoprotein view function
@login_required
def delete_phosphoprotein(request, user_id, pk):
    phosphoprotein = get_object_or_404(PhosphoProtein, pk=pk)

    if request.user == phosphoprotein.submitted_by:
        phosphoprotein.delete()
        messages.success(request, "The phosphoprotein has been deleted.")
    else:
        messages.error(request, "You have no power here.")

    return redirect('profile', pk=user_id)