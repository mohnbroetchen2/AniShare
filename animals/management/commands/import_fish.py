from django.core.management.base import BaseCommand
from django.db.models import Q
from animals.models import Animal, Person, Location
from datetime import datetime
import xlrd
from xlrd import xldate_as_datetime

class Command(BaseCommand):
    help = 'Import existing data from mice2giveaway excel list'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        lines_count = 0
        fname = options['filename'][0]
        xl = xlrd.open_workbook(fname) # Open the workbook
#        for sheet in (2,0):
        for sheet in (0,):
            print('Sheet #' + str(sheet))
            xl_sheet = xl.sheet_by_index(sheet) # grab sheet

            num_cols = xl_sheet.ncols   # Number of columns
            for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows
                print('.', end ="", flush=True)
#                print ('-'*40)
#                print ('Row: %s' % row_idx)   # Print row number
#                for col_idx in range(0, num_cols):  # Iterate through columns
#                    cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
#                    print ('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))

                a = Animal()

#                a.pk = int(xl_sheet.cell(row_idx, 0).value)
                #a.entry_date = xldate_as_datetime(xl_sheet.cell(row_idx, 1).value, xl.datemode) 
		#a.available_from = xldate_as_datetime(xl_sheet.cell(row_idx, 0).value, xl.datemode) # angeboten am
                a.animal_type = 'fish'
                a.available_from = datetime.today().date()
                a.comment = str(xl_sheet.cell(row_idx, 0).value).strip() # Geschlecht		
                a.sex = str(xl_sheet.cell(row_idx, 1).value).strip().lower() or 'u' # Geschlecht
                a.line = str(xl_sheet.cell(row_idx, 2).value).strip() # Zuchtlinie
                a.lab_id = str(xl_sheet.cell(row_idx, 3).value).strip() # Käfig-ID
                a.database_id = str(xl_sheet.cell(row_idx, 4).value).strip() # Tier-ID
                a.day_of_birth = xldate_as_datetime(xl_sheet.cell(row_idx, 5).value, xl.datemode) #Geb.
                a.amount = int(xl_sheet.cell(row_idx, 7).value) # Anzahl
                a.licence_number = str(xl_sheet.cell(row_idx, 11).value).strip() # Aktenzeichen               
                location_name = str(xl_sheet.cell(row_idx, 13).value).strip() # Raum
                responsible_person = str(xl_sheet.cell(row_idx, 16).value).strip().strip() # Verantwortliche Person
                #a.available_from = xldate_as_datetime(xl_sheet.cell(row_idx, 19).value, xl.datemode)
                a.available_to = xldate_as_datetime(xl_sheet.cell(row_idx, 22).value, xl.datemode)
                #a.new_owner = str(xl_sheet.cell(row_idx, 21).value).strip()
                
#                a.organ_type = 'whole animal'

                #a.mutations = 

                
                try:
                    a.location = Location.objects.get(name=location_name)
                except Location.DoesNotExist:
                    loc = Location(name=location_name)
                    loc.save()
                    a.location = loc

                a.responsible_person = Person.objects.get(Q(email=responsible_person.lower()) | Q(name__iexact=responsible_person.lower()))
                try:
                    Animal.objects.get(entry_date=a.entry_date,
                                       day_of_birth=a.day_of_birth,
                                       available_from=a.available_from,
                                       available_to=a.available_to,
                                       line=a.line,
                                       database_id=a.database_id,
                                       lab_id=a.lab_id,
                                       location=a.location,
                                       sex=a.sex)
                except Animal.DoesNotExist:
                    a.save()
                    lines_count += 1
            print()

        self.stdout.write(self.style.SUCCESS('Successfully imported %i lines.' % lines_count))
