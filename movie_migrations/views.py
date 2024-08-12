from django.http import HttpResponse
from django.views.generic import FormView
from .forms import MigrationForm
import csv
from movies.models import Movie
from ratings.models import Rating
from links.models import Link
from tags.models import Tag, GenomeScore, GenomeTag
import datetime
import pytz
import time
from django.db import connection

class CSVHandlerMixIn:
    
    def handle_movie_file(self, file, model, columns):
        start = time.time( )
        decoded_file = file.read().decode('utf-8').splitlines()
        
        batch_size = 10000 
        rows = []

        reader = csv.DictReader(decoded_file)
        for row in reader:
            values = list(row.values())
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
    
    def handle_movie_file_2(self, file, model):
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
        
        movies_dict = {movie.id: movie.id for movie in Movie.objects.all()}
        
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        batch_size = 10000 
        rows = []

        print('Iniciando a leitura do arquivo')
        for row in reader:
            movieId = int(row.get('movieId'))
            timestamp = None
            if 'timestamp' in row.keys():
                timestamp = row.pop('timestamp')
            
            if timestamp:
                timestamp = datetime.datetime.fromtimestamp(int(timestamp))
                timestamp = pytz.utc.localize(timestamp)
            
            if movieId in movies_dict.keys():
                values = list(row.values())
                if timestamp:
                    values.append(timestamp)    
                rows.append(values)
            
            if len(rows) >= batch_size:
                print(f'Inserindo registros')
                self.bulk_insert(model, rows, columns)
                rows = []  

        if rows:
            self.bulk_insert(model, rows, columns)
        
        end = time.time()
        return end-start
    
    def bulk_insert(self, model, rows, columns):
        table_name = model._meta.db_table
        
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (%s)"
        
        placeholders = ", ".join(["%s"] * len(columns))
        
        with connection.cursor() as cursor:
            cursor.executemany(sql % placeholders, rows)
                
    def handle_tag_depedent_file(self, file, model, columns):
        start = time.time()
        decoded_file = file.read().decode('utf-8').splitlines()
        
        tags_dict = {tag.id: tag.id for tag in Tag.objects.all()}
        batch_size = 10000 
        rows = []
        
        reader = csv.DictReader(decoded_file)
        for row in reader:
            tagId = int(row.get('tagId'))
            if tagId in tags_dict.keys():
                values = list(row.values())
                rows.append(values)
                
        if len(rows) >= batch_size:
            print(f'Inserindo registros')
            self.bulk_insert(model, rows, columns)
            rows = []  
                
        end = time.time()
        return end-start

class MigrationView(FormView, CSVHandlerMixIn):
    template_name = "base.html"
    form_class = MigrationForm
    success_url = "/"
    
    def form_valid(self, form):
        if form.cleaned_data['movies']:
            self.handle_movie_file(form.cleaned_data['movies'], Movie, ['id', 'title', 'genres'])
        if form.cleaned_data['ratings']:
            self.handle_movie_depedent_file(form.cleaned_data['ratings'], Rating, ['user_id', 'movie_id', 'rating', 'timestamp'])
        if form.cleaned_data['links']:
            self.handle_movie_depedent_file(form.cleaned_data['links'], Link, ['movie_id', 'imdb_id', 'tmdb_id'])
        if form.cleaned_data['tags']:
            self.handle_movie_depedent_file(form.cleaned_data['tags'], Tag, ['user_id', 'movie_id', 'tag', 'timestamp'])
        if form.cleaned_data['genome_tags']:
            self.handle_tag_depedent_file(form.cleaned_data['genome_tags'], GenomeTag, ['tag_id', 'tag_details'])
        if form.cleaned_data['genome_scores']:
            self.handle_tag_depedent_file(form.cleaned_data['genome_scores'], GenomeScore,  ['movie_id', 'tag_id', 'relevance'])
        
        return super().form_valid(form)
