from  kolibri_report.report import Report
from kolibri.model_trainer import ModelTrainer,ModelConfig
from kolibri.model_loader import ModelLoader
import os
import pandas as pd

data = pd.read_csv('/Users/aneruthmohanasundaram/Documents/Office/kolibri_doc/wine.csv')

confg = {}
confg['do-lower-case'] = True
confg['language'] = 'en'
confg['filter-stopwords'] = True
confg["model"] = 'RandomForestClassifier'
confg["n_estimators"] = 100
confg['output-folder'] = '/Users/aneruthmohanasundaram/Documents/Office/kolibri_doc/demos'
confg['pipeline']= ['SklearnEstimator']
confg['target']= 'type'
confg['evaluate-performance'] = True

X = data.drop('type',axis=1)
y = data.type

trainer=ModelTrainer(ModelConfig(confg))

trainer.fit(X, y)

model_directory = trainer.persist(confg['output-folder'], fixed_model_name="Streamlit test")
model_interpreter = ModelLoader.load(os.path.join(confg['output-folder'], 'Streamlit test'))

app_report = Report(data,model_interpreter)
app_report.run()