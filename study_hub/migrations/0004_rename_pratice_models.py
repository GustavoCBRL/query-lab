from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("study_hub", "0003_praticeexercise_praticesubmission_delete_pratices"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PraticeExercise",
            new_name="PracticeExercise",
        ),
        migrations.RenameModel(
            old_name="PraticeSubmission",
            new_name="PracticeSubmission",
        ),
        migrations.RenameField(
            model_name="practicesubmission",
            old_name="pratice",
            new_name="practice",
        ),
        migrations.AlterField(
            model_name="practiceexercise",
            name="topic",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="practices",
                to="study_hub.topics",
            ),
        ),
    ]