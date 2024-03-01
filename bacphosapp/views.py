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

def home(request):
    return render(request, 'home.html', {})

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
    
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

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

class ProteinsListView(ListView):
    model = PhosphoProtein
    template_name = "protein_list.html"
    context_object_name = "proteins"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        uniprot_code = self.request.GET.get("uniprot_code")
        gene_name = self.request.GET.get("gene_name")
        protein_name = self.request.GET.get("protein_name")
        modification_type = self.request.GET.get("modification_type")

        combined_query = Q()

        if uniprot_code:
            combined_query |= Q(uniprot_code__icontains=uniprot_code)
        if gene_name:
            combined_query |= Q(gene_name__icontains=gene_name)
        if protein_name:
            combined_query |= Q(protein_name__icontains=protein_name)
        if modification_type and modification_type != '': 
            combined_query |= Q(phosphosite__modification_type__iexact=modification_type)

        return queryset.filter(combined_query).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProteinSearchForm(self.request.GET)
        if not context["proteins"]:
            error_message = "There is no data available."
            messages.error(self.request, error_message)
            context["error_message"] = error_message

        phosphosites_dict = {}
        for protein in context["proteins"]:
            phosphosites = list(PhosphoSite.objects.filter(protein=protein))
            phosphosites.sort(key=lambda x: x.modification_type)
            phosphosites_dict[protein.pk] = phosphosites 

            context["phosphosites_dict"] = phosphosites_dict

        return context
    
class ProteinDetailView(DetailView):
    model = PhosphoProtein
    template_name = "protein_details.html"
    context_object_name = "protein"

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['pk'])

def overview(request):
    return render(request, 'overview.html')

def resources(request):
    return render(request, 'resources.html')

def cite(request):
    return render(request, 'cite.html')

def guide(request):
    return render(request, 'guide.html')

def search_phosphoprotein(request):
    if request.method == 'GET':
        uniprot_id = request.GET.get('Uniprot_Code')
        gene_name = request.GET.get('Gene_Name')
        protein_name = request.GET.get('Protein_Name')
        queryset = PhosphoProtein.objects.all()

        if uniprot_id:
            queryset = queryset.filter(uniprot_code__icontains=uniprot_id)

        if gene_name:
            queryset = queryset.filter(gene_name__icontains=gene_name)

        if protein_name:
            queryset = queryset.filter(protein_name__icontains=protein_name)

        phospho_proteins = queryset

        if not phospho_proteins:
            messages.error(request, "No data available.")

        return render(request, 'protein_list.html', {'phospho_proteins': phospho_proteins})

    return render(request, 'home.html')

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
