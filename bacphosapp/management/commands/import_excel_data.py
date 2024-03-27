from django.core.management.base import BaseCommand
import pandas as pd
from bacphosapp.models import PhosphoProtein

class Command(BaseCommand):
    help = 'Import data from Excel file to PostgreSQL database'

    def handle(self, *args, **options):
        excel_file = 'C:\\Users\\patzo\\Documents\\asus\\documents\\pai\\data\\pedb_cured.xlsx'  
        df = pd.read_excel(excel_file)
        df['approved'] = df['approved'].fillna(False)

        existing_records = {}

        for _, row in df.iterrows():
            uniprot_code = row['uniprot_code']
            gene_name = row['gene_name']
            protein_name = row['protein_name']
            position = row['position']
            existing_record = existing_records.get((uniprot_code, gene_name, protein_name, position))

            if existing_record:
                existing_record.uniprot_url = row['uniprot_url']
                existing_record.window_5_aa = row['window_5_aa']
                existing_record.modification_type = row['modification_type']
                existing_record.method = row['method']
                existing_record.sequence = row['sequence']
                existing_record.pdb_code = row['pdb_code']
                existing_record.pdb_url = row['pdb_url']
                existing_record.submitted_by = None
                existing_record.approved = row['approved']
                existing_record.reference = row['reference']
                existing_record.save()
            else:
                new_record = PhosphoProtein.objects.create(
                    uniprot_code=uniprot_code,
                    uniprot_url=row['uniprot_url'],
                    gene_name=gene_name,
                    protein_name=protein_name,
                    position=position,
                    window_5_aa=row['window_5_aa'],
                    modification_type=row['modification_type'],
                    method=row['method'],
                    sequence=row['sequence'],
                    pdb_code=row['pdb_code'],
                    pdb_url=row['pdb_url'],
                    submitted_by=None,
                    approved=row['approved'],
                    reference=row['reference'],
                    alphafold_url=row['alphafold_url'],
                )
                existing_records[(uniprot_code, gene_name, protein_name, position)] = new_record

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
