from django import forms

class MigrationForm(forms.Form):
    movies = forms.FileField(label="Filmes", required=False)
    ratings = forms.FileField(label="Avaliações", required=False)
    links = forms.FileField(label="Links", required=False)
    tags = forms.FileField(label="Tags", required=False)
    genome_tags = forms.FileField(label="Genome Tags", required=False)
    genome_scores = forms.FileField(label="Genome Scores", required=False)