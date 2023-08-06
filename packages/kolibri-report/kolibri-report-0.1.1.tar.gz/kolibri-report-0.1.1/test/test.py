from kolibri_report.report import Report
from kolibri.model_trainer import ModelTrainer,ModelConfig
from kolibri.model_loader import ModelLoader
import os
from kolibri.datasets import get_data

data = get_data('amazon')

confg = {}
confg['do-lower-case'] = True
confg['language'] = 'en'
confg['filter-stopwords'] = True
confg["model"] = 'RandomForestClassifier'
confg["n_estimators"] = 100
confg['output-folder'] = '/Users/aneruthmohanasundaram/Documents/koli_report_test'
confg['pipeline']= ['WordTokenizer', 'TFIDFFeaturizer', 'SklearnEstimator']
confg['evaluate-performance'] = True

X = data.reviewText.values.tolist()
y = data.Positive.values.tolist()

trainer = ModelTrainer(ModelConfig(confg))

trainer.fit(X, y)

model_directory = trainer.persist(confg['output-folder'], fixed_model_name="Streamlit test")
# print(model_directory)
model_interpreter = ModelLoader.load(os.path.join(confg['output-folder'], 'Streamlit test'))

app_report = Report(data,model_interpreter,model_directory)
app_report.run()