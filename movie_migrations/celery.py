
import sys
from movies.models import Movie
from ratings.models import Rating
from links.models import Link
from tags.models import Tag, GenomeScore, GenomeTag
from movie_migrations.models import MovieMigration
from django.db import connection
import re
import time
import csv
import datetime
import pytz
from celery import shared_task
from .models import MovieMigration
import logging

logger = logging.getLogger(__name__)
    
def csv_validator(row, model, instances):
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
            return False
        
        if not re.match(r'^\d+$', row['userId']):
            return False
        
        
        if float(row['rating']) < 0 or float(row['rating']) > 5:
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
        
        if int(row['movieId']) not in instances:
            return False
        
        
    
    return True

def execute(model, rows, columns):
    sql = f"INSERT INTO {model._meta.db_table} ({', '.join(columns)}) VALUES {', '.join(rows)}"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        
def update_migration(migration, data_count, failures, start):
    end = time.time()
    migration.total_time = end-start
    migration.data_quantity = data_count
    migration.registry_erros_number = failures
    migration.status = MovieMigration.Status.COMPLETED
    migration.save()
    
@shared_task
def handle_movie_file(migration_id, columns):
    start = time.time( )
    migration = MovieMigration.objects.get(id=migration_id)
    decoded_file = migration.file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    
    batch_size = 10000 
    failures, data_count = 0, 0
    rows = []
    
    movies_dict = [movie.id for movie in Movie.objects.all()]

    for row in reader:
        if csv_validator(row, Movie, movies_dict):
            
            match = re.search(r'\b(19|20)\d{2}\b', row['title'])
            
            if match:
                row['release_year'] = match.group(0)
            else:
                row['release_year'] = 'null'
                
            row['title'] = row['title'].replace("'", "''")
            row['genres'] = row['genres'].replace("'", "''")
            
            rows.append(
                f"({row['movieId']}, '{row['title']}', '{row['genres']}', {row['release_year']})"
            )
            data_count += 1
            
        else:
            failures += 1
        
        if len(rows) >= batch_size:
            execute(Movie, rows, columns)
            rows = []
    
    if rows:
        execute(Movie, rows, columns)
        rows = []

    update_migration(migration, data_count, failures, start)

@shared_task
def handle_movie_depedent_file(migration_id, columns):
    start = time.time()
    
    movies_dict = {movie.id: movie.id for movie in Movie.objects.all()}
    
    migration = MovieMigration.objects.get(id=migration_id)
    decoded_file = migration.file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    
    model = Tag
    if migration.model == 'Avaliações':
        model = Rating
    
    batch_size = 10000 
    rows = []
    failures, data_count = 0, 0

    for row in reader:
        movieId = row.get('movieId', None)
        timestamp = row.pop('timestamp', None)
        
        if movieId and timestamp and re.match(r'^\d+$', timestamp) and re.match(r'^\d+$', row['movieId']) and int(movieId) in movies_dict.keys():
            if csv_validator(row, model, movies_dict):
                timestamp = datetime.datetime.fromtimestamp(int(timestamp))
                timestamp = pytz.utc.localize(timestamp)
                                       
                if model == Tag:
                    row['tag'] = row['tag'].replace("'", "''")
                    rows.append(
                        f"({row['userId']}, {row['movieId']}, '{row['tag']}', '{timestamp}')"
                    )
                else:
                    rows.append(
                        f"({row['userId']}, {row['movieId']}, {row['rating']}, '{timestamp}')"
                    )
                data_count += 1
                
            else:
                failures += 1
                
        else:
            failures += 1
            
        if len(rows) >= batch_size:
            execute(model, rows, columns)
            rows = []  

    if rows:
        execute(model, rows, columns)
        rows = []
    
    update_migration(migration, data_count, failures, start)

@shared_task
def handle_link_file(migration_id, columns):
    start = time.time()
    
    movies_dict = {movie.id: movie.id for movie in Movie.objects.all()}
    
    model = Link
    
    migration = MovieMigration.objects.get(id=migration_id)
    decoded_file = migration.file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    
    batch_size = 10000 
    rows = []
    failures, data_count = 0, 0

    for row in reader:
        movieId = row.get('movieId', None)
        
        if movieId and re.match(r'^\d+$', row['movieId']) and int(movieId) in movies_dict.keys():
            if csv_validator(row, model, movies_dict):
                rows.append(
                    f"({row['movieId']}, {row['imdbId']}, {row['tmdbId']})"
                )
                data_count += 1
            else:
                failures += 1
        else:
            failures += 1
            
        if len(rows) >= batch_size:
            execute(model, rows, columns)
            rows = []  

    if rows:
        execute(model, rows, columns)
        rows = []
    
    update_migration(migration, data_count, failures, start)

@shared_task
def handle_tag_depedent_file(migration_id, columns):
    start = time.time()
    
    migration = MovieMigration.objects.get(id=migration_id)
    decoded_file = migration.file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    
    tags_dict = {tag.id: tag.id for tag in Tag.objects.all()}
    movies_dict = {movie.id: movie.id for movie in Movie.objects.all()}
    
    batch_size = 10000 
    rows = []
    failures, data_count = 0, 0
    
    model = GenomeTag
    if migration.model == 'Pontuações do Genoma':
        model = GenomeScore
        
    for row in reader:
        tagId = row.get('tagId', None)
        if tagId and int(tagId) in tags_dict.keys():
            if csv_validator(row, model, movies_dict):
                if model == GenomeTag:
                    row['tag'] = row['tag'].replace("'", "''")
                    rows.append(
                        f"({row['tagId']}, '{row['tag']}')"
                    )
                else: 
                    rows.append(
                        f"({row['movieId']}, {row['tagId']}, {row['relevance']})"
                    )
                data_count += 1
            else:
                failures += 1
        else:
            failures += 1
            
        if len(rows) >= batch_size:
            execute(model, rows, columns)
            rows = []  
            
    if rows:
        execute(model, rows, columns)
        row = []

    update_migration(migration, data_count, failures, start)