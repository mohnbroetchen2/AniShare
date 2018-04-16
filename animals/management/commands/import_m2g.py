from django.core.management.base import BaseCommand
from django.db.models import Q
from animals.models import Animal, Person, Lab
import datetime
import xlrd
from xlrd import xldate_as_tuple, xldate_as_datetime

class Command(BaseCommand):
    help = 'Import existing data from mice2giveaway excel list'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        lines_count = 0
        fname = options['filename'][0]
        xl = xlrd.open_workbook(fname) # Open the workbook
        xl_sheet = xl.sheet_by_index(0) # grab first sheet

        num_cols = xl_sheet.ncols   # Number of columns
        for row_idx in range(10, xl_sheet.nrows):    # Iterate through rows
            print ('-'*40)
            print ('Row: %s' % row_idx)   # Print row number
            for col_idx in range(0, num_cols):  # Iterate through columns
                cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
                print ('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))

            a = Animal()

            a.pk = int(xl_sheet.cell(row_idx, 0).value)
            a.entry_date = xldate_as_datetime(xl_sheet.cell(row_idx, 1).value, xl.datemode)
            a.pyrat_id = str(xl_sheet.cell(row_idx, 2).value).strip()
            a.lab_id = str(xl_sheet.cell(row_idx, 3).value).strip()
            a.day_of_birth = xldate_as_datetime(xl_sheet.cell(row_idx, 4).value, xl.datemode)
            age = int(xl_sheet.cell(row_idx, 5).value)
            a.line = str(xl_sheet.cell(row_idx, 6).value).strip()
            mutation_1 = str(xl_sheet.cell(row_idx, 7).value).strip()
            grade_1 = str(xl_sheet.cell(row_idx, 8).value).strip()
            mutation_2 = str(xl_sheet.cell(row_idx, 9).value).strip()
            grade_2 = str(xl_sheet.cell(row_idx, 10).value).strip()
            mutation_3 = str(xl_sheet.cell(row_idx, 11).value).strip()
            grade_3 = str(xl_sheet.cell(row_idx, 12).value).strip()
            mutation_4 = str(xl_sheet.cell(row_idx, 13).value).strip()
            grade_4 = str(xl_sheet.cell(row_idx, 14).value).strip()
            a.sex = str(xl_sheet.cell(row_idx, 15).value).strip()
            a.location = str(xl_sheet.cell(row_idx, 16).value).strip()
            a.licence_number = str(xl_sheet.cell(row_idx, 17).value).strip()
            responsible_person = str(xl_sheet.cell(row_idx, 18).value).strip().strip()
            a.available_from = xldate_as_datetime(xl_sheet.cell(row_idx, 19).value, xl.datemode)
            a.available_to = xldate_as_datetime(xl_sheet.cell(row_idx, 20).value, xl.datemode)
            a.new_owner = str(xl_sheet.cell(row_idx, 21).value).strip()

            a.mutation =  mutation_1 + ' ' + grade_1 + '\n'
            a.mutation += mutation_2 + ' ' + grade_2 + '\n'
            a.mutation += mutation_3 + ' ' + grade_3 + '\n'
            a.mutation += mutation_4 + ' ' + grade_4 + '\n'


            a.responsible_person = Person.objects.get(Q(email=responsible_person.lower()) | Q(name__iexact=responsible_person.lower()))
            a.save()


            #print(nr, entry_date, id, lab_id, dob, age, line, mutation, sex, building, licence_number, responsible_person, available_from, available_until, new_owner)

            lines_count += 1


        self.stdout.write(self.style.SUCCESS('Successfully imported %i lines.' % lines_count))
