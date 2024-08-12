from django.http import HttpResponse
from django.views.generic import FormView, ListView
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
import re


class CSVHandlerMixIn:
    
    def csv_validator(self, row, model, instances):
        if model == Movie:
            if 'movieId' not in row.keys() or 'title' not in row.keys() or 'genres' not in row.keys():
                return False
            
            if not re.match(r'^\d+$', row['movieId']):
                return False
            
            if int(row['movieId']) in instances:
                return False
            
            if not re.match(r'^[\w\-]+(\|[\w\-]+)*$', row['genres']):
                return False


        elif model == Rating:
            if 'userId' not in row.keys() or 'rating' not in row.keys():
                print('Campos faltando')
                return False
            
            if not re.match(r'^\d+$', row['userId']):
                print('userId invalido')
                return False
            
            
            if float(row['rating']) < 0 or float(row['rating']) > 5:
                print('rating invalido')
                return False
            
        elif model == Link:
            if 'imdbId' not in row.keys() or 'tmdbId' not in row.keys():
                return False
            
            if not re.match(r'^\d+$', row['imdbId']):
                return False
            
            if not re.match(r'^\d+$', row['tmdbId']):
                return False
            
        elif model == Tag:
            if 'userId' not in row.keys() or 'tag' not in row.keys():
                return False
            
            if not re.match(r'^\d+$', row['userId']):
                return False
        
        elif model == GenomeScore:
            if 'relevance' not in row.keys() and 'movieId' not in row.keys():
                return False
            
            if float(row['relevance']) < 0 or float(row['relevance']) > 1:
                return False
            
            if not re.match(r'^\d+$', row['movieId']):
                return False
            
            if int(row['movieId']) in instances:
                return False
            
            
      
        return True
        
    
    def handle_movie_file(self, file, model, columns):
        start = time.time( )
        decoded_file = file.read().decode('utf-8').splitlines()
        
        batch_size = 10000 
        rows = []
        failures = 0
        
        movies_dict = [movie.id for movie in Movie.objects.all()]

        reader = csv.DictReader(decoded_file)
        for row in reader:
            if self.csv_validator(row, model, movies_dict):
                values = list(row.values())
                rows.append(values)
            else:
                failures += 1
             
            if len(rows) >= batch_size:
                print(f'Inserindo registros')
                self.bulk_insert(model, rows, columns)
                rows = []  
        
        if rows:
            self.bulk_insert(model, rows, columns)
    
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
        failures = 0

        print('Iniciando a leitura do arquivo')
        for row in reader:
            movieId = row.get('movieId', None)
            if 'timestamp' in row.keys():
                timestamp = row.pop('timestamp')
            
            if movieId and re.match(r'^\d+$', timestamp) and re.match(r'^\d+$', row['movieId']) and int(movieId) in movies_dict.keys():
                if self.csv_validator(row, model, movies_dict):
                    if timestamp:
                        timestamp = datetime.datetime.fromtimestamp(int(timestamp))
                        timestamp = pytz.utc.localize(timestamp)
                
                    values = list(row.values())
                    if timestamp:
                        values.append(timestamp)    
                    rows.append(values)
                else:
                    failures += 1
            else:
                failures += 1
                
            if len(rows) >= batch_size:
                print(f'Inserindo registros')
                self.bulk_insert(model, rows, columns)
                rows = []  

        if rows:
            self.bulk_insert(model, rows, columns)
        
        end = time.time()
        return end-start
    
    
    def handle_link_file(self, file, model, columns):
        start = time.time()
        
        movies_dict = {movie.id: movie.id for movie in Movie.objects.all()}
        
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        batch_size = 10000 
        rows = []
        failures = 0

        print('Iniciando a leitura do arquivo')
        for row in reader:
            movieId = row.get('movieId', None)
            
            if movieId and re.match(r'^\d+$', row['movieId']) and int(movieId) in movies_dict.keys():
                if self.csv_validator(row, model, movies_dict):
                    values = list(row.values()) 
                    rows.append(values)
                else:
                    failures += 1
            else:
                failures += 1
                
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
        movies_dict = {movie.id: movie.id for movie in Movie.objects.all()}
        
        batch_size = 10000 
        rows = []
        failures = 0
        
        reader = csv.DictReader(decoded_file)
        for row in reader:
            tagId = row.get('tagId', None)
            
            
            if int(tagId) in tags_dict.keys():
                print('Validando')
                if self.csv_validator(row, model, movies_dict):
                    print('Validado2')
                    values = list(row.values())
                    rows.append(values)
                else:
                    failures += 1
            else:
                failures += 1
                
            if len(rows) >= batch_size:
                print(f'Inserindo registros')
                self.bulk_insert(model, rows, columns)
                rows = []  
                
        if rows:
            self.bulk_insert(model, rows, columns)
                
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
            self.handle_link_file(form.cleaned_data['links'], Link, ['movie_id', 'imdb_id', 'tmdb_id'])
        if form.cleaned_data['tags']:
            self.handle_movie_depedent_file(form.cleaned_data['tags'], Tag, ['user_id', 'movie_id', 'tag', 'timestamp'])
        if form.cleaned_data['genome_tags']:
            self.handle_tag_depedent_file(form.cleaned_data['genome_tags'], GenomeTag, ['tag_id', 'tag_details'])
        if form.cleaned_data['genome_scores']:
            self.handle_tag_depedent_file(form.cleaned_data['genome_scores'], GenomeScore,  ['movie_id', 'tag_id', 'relevance'])
        
        return super().form_valid(form)

class InfoFile(ListView):
    template_name = "table_file.html"
    model = Movie
    context_object_name = "movies"