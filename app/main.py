import logging

from app.database.email_database import EmailDatabase
from app.model.model_manager import ModelManager
from app.model.zero_shot_model import ZeroShotModel
from app.orchestration.preprocessor.simple_preprocessor import SimplePreprocessor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    db_client = EmailDatabase()
    preprocessor = SimplePreprocessor()
    model_directory = "./models"
    # model_name = "bert"
    # model_name = "logistic_regression" # also need sensitive
    # model_name = "zero_shot"
    # model_name = "few_shot"
    model_name = "one_class_svm"
    retrain = True
    app = ModelManager(email_db=db_client, preprocessor=preprocessor, model_name=model_name, retrain=retrain)
    if not app.model.is_trained and not isinstance(app.model, ZeroShotModel) or retrain:
        logger.info("not zero shot model")
        app.train_model()

    new_email_text = ("Liebe Studienberatung, wie viele Credits muss ich in meinem Master in Informatik machen? Ich "
                      "bin im 4. Semester. Zusätzlich habe ich ein Spanischkurs belegt und möchte mir den gerne "
                      "anrechnen lassen. Geht das? Vielen Dank! Grüße, Peter Lustig")
    new_email_text2 = ("Liebe Studienberatung, ich habe psychische Probleme und werde von meinen Mitstudierenden "
                       "gemobbt. Ich denke darüber nach mein Studium abzubrechen. Meine Eltern sind gestorben, "
                       "kann ich ein Pausensemester nehmen?")
    classification, certainty = app.classify_email(new_email_text)
    print(f"Classification: {classification}, Certainty: {certainty:.10f}")
    classification, certainty = app.classify_email(new_email_text2)
    print(f"Classification: {classification}, Certainty: {certainty:.10f}")
