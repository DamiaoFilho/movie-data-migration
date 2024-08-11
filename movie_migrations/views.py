from django.http import HttpResponse
from django.views.generic import FormView
from .forms import MigrationForm
import csv
from movies.models import Movie
from ratings.models import Rating
from tags.models import Tag
import datetime
import pytz
import time
from django.db import connection

class CSVHandlerMixIn:
    
    def handle_movie_file(self, file, model):
        start = time.time( )
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            model.objects.create(**row)
        end = time.time()
        print(end-start)
        return end-start
    
    def handle_movie_depedent_file(self, file, model, columns):
        start = time.time()
        
        movies_dict = {movie.movieId: movie.movieId for movie in Movie.objects.all()}
        
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        batch_size = 10000 
        rows = []

        print('Iniciando a leitura do arquivo')
        for row in reader:
            movieId = int(row.pop('movieId'))
            timestamp = row.pop('timestamp')
            
            if timestamp:
                timestamp = datetime.datetime.fromtimestamp(int(timestamp))
                timestamp = pytz.utc.localize(timestamp)
            
            if movieId in movies_dict.keys():
                movie_db_id = movies_dict[movieId]
                values = [
                    int(row.get('userId')),            
                    float(row.get('rating')),           
                    timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else None,
                    movie_db_id,                 
                ]
                rows.append(values)
            
            if len(rows) >= batch_size:
                print(f'Inserindo registros')
                self.bulk_insert(model, rows, columns)
                rows = []  

        if rows:
            self.bulk_insert(model, rows, columns)
        
        end = time.time()
        print(end-start)
        return end-start
    
    def bulk_insert(self, model, rows, columns):
        table_name = model._meta.db_table
        
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (%s)"
        
        placeholders = ", ".join(["%s"] * len(columns))
        
        with connection.cursor() as cursor:
            cursor.executemany(sql % placeholders, rows)
                
    def handle_tag_depedent_file(self, file, model):
        start = time.time()
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            tagId = row.pop('tagId')
            if tagId:
                tagId = Tag.objects.filter(tagId=tagId).first()
                model.objects.create(tagId=tagId, **row)
                
        end = time.time()
        print(end-start)
        return end-start

class MigrationView(FormView, CSVHandlerMixIn):
    template_name = "base.html"
    form_class = MigrationForm
    success_url = "/"
    
    def form_valid(self, form):
        self.handle_movie_depedent_file(form.cleaned_data['ratings'], Rating, ['user_id', 'rating', 'timestamp', 'movie_id'])
        # self.handle_movie_depedent_file(form.cleaned_data['links'], Link)
        # self.handle_movie_depedent_file(form.cleaned_data['tags'], Tag)
        # self.handle_csv_file(form.cleaned_data['genome_tags'], GenomeTag)
            # self.handle_csv_file(form.cleaned_data['genome_scores'], GenomeScore)
        # self.handle_movie_file(form.cleaned_data['movies'], Movie)
        
        return super().form_valid(form)
