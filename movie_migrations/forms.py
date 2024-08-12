from django import forms

class MigrationForm(forms.Form):
    DATA_TYPE_CHOICES = [
        ('movie', 'Filme'),
        ('links', 'Link'),
        ('tags', 'Tag'),
        ('ratings', 'Avaliação'),
        ('genome_tags', 'Genome Tags'),
        ('genome_scores', 'Genome Scores'),
    ]
    data_type = forms.ChoiceField(label="Tipo", choices=DATA_TYPE_CHOICES)    
    file = forms.FileField(label="Arquivo")
