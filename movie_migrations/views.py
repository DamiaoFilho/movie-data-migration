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
    
    def handle_movie_depedent_file(self, file, model):
        start = time.time()
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            movieId = row.pop('movieId')
            timestamp = row.pop('timestamp')
            
            if timestamp:
                timestamp = datetime.datetime.fromtimestamp(int(timestamp))
                timestamp = pytz.utc.localize(timestamp)

                if movieId:
                    movie = Movie.objects.filter(movieId=movieId).first()
                    model.objects.create(movieId=movie, timestamp=timestamp,**row)
            
            elif movieId:
                movie = Movie.objects.filter(movieId=movieId).first()
                model.objects.create(movieId=movie, **row)
        end = time.time()
        print(end-start)
        return end-start
                
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
    
    def form_valid(self, form):
        self.handle_movie_depedent_file(form.cleaned_data['ratings'], Rating)
        # self.handle_movie_depedent_file(form.cleaned_data['links'], Link)
        # self.handle_movie_depedent_file(form.cleaned_data['tags'], Tag)
        # self.handle_csv_file(form.cleaned_data['genome_tags'], GenomeTag)
            # self.handle_csv_file(form.cleaned_data['genome_scores'], GenomeScore)
        # self.handle_movie_file(form.cleaned_data['movies'], Movie)
        
        return super().form_valid(form)
