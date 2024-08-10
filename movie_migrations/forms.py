from django import forms

class MigrationForm(forms.Form):
    movies = forms.FileField(label="Filmes")
    ratings = forms.FileField(label="Avaliações")
    links = forms.FileField(label="Links")
    tags = forms.FileField(label="Tags")
    genome_tags = forms.FileField(label="Genome Tags")
    genome_scores = forms.FileField(label="Genome Scores")