from abc import ABC,abstractclassmethod
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from kolibri.model_trainer import ModelTrainer,ModelConfig
from kolibri.model_loader import ModelLoader
import seaborn as sns,os

class KolibriImplements(ABC):
    """
    This is a abstract method for report implementation.
    """
    @abstractclassmethod
    def data(self):
        pass

    @abstractclassmethod
    def visualise(self):
        pass

    @abstractclassmethod
    def modelAnalysis(self):
        pass
    
    @abstractclassmethod
    def featureInteraction(self):
        pass

    @abstractclassmethod
    def run(self):
        pass

class Report(KolibriImplements):
    """
    A class which creates us the dashboard for our model and plots all the score and graph. This requires
    dataset as important parameter.
    """
    def __init__(self,data=None,model_interpreter=None,trainer=None) -> None:
        """A constructor which takes the data, model_interpreter and the trainer as important parameter and 

        Args:
            data (Dataframe, optional): Pandas Dataframe(Dataset). Defaults to None.
            model_interpreter (kolibri.model_loader.ModelLoader, optional): ModelLoader which is a trained pipeline of components to parse text documents.. Defaults to None.
            trainer (kolibri.model_trainer.ModelTrainer, optional): A paramneter which informs about pipeline specification and configuration. Defaults to None.
        """
        self.dataset = data
        self.model_interpreter = model_interpreter
        self.trainer = trainer
        # self.count_plot = None
        
    
    def data(self):
        '''
        This method displays description of the model, Model Version​,Kolibri Version​,Owner​ and Trained at​.
        '''
        # st.dataframe(self.dataset,width=1000)
        st.table(self.dataset[:21])
    
    def visualise(self):
        st.title('Visualising our dataset!!')
        # if we choose the options we get our output result as list
        col1,col2 = st.columns([2,2])
        with col1:
            st.write(''' #### Class comparison for our dataset''')
            sns.countplot(x='type',data=self.dataset)
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
        with col2:
            st.write(''' #### Heatmap for our dataset''')
            sns.heatmap(self.dataset.corr(),cmap='Greens')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
    
    def modelAnalysis(self,y,data_pred,label):
        """This is a function where it plots all the score analysis such as __*precision,recall,f1-score and 
        accuracy*__.

        Args:
            y (Pandas series): target varaible values can be pass either as pandas series or list
            data_pred (List): Prediction values of our target variable
            label (List): Unique values of our label column
        """
        # from kolibri.evaluators.classifier_evaluator import ClassifierEvaluator
        # scores_values = ClassifierEvaluator.classification_report(y,data_pred,label)
        # scores = pd.DataFrame.from_dict(scores_values)
        # scores.drop(scores.index[len(scores)-1],inplace=True) # dropping the support value
        # newScores = pd.DataFrame(scores.drop(columns=['accuracy', 'macro avg', 'weighted avg']))
        # newScores.plot.bar()
        # st.pyplot()
        target_folder = self.trainer.config['output-folder']
        st.write(target_folder)

    
    def featureInteraction(self):
        """Checking our feature how it interacts with other feature. We provde you a dropbox 
        functionality and then you can analyse the interactn fo the features.
        """
        st.title('Feature Interactions for our datset!!')
        st.header('Upcoming feature')

    def run(self):
        st.set_page_config(layout='wide')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        col1,col2,col3,col4,col5 = st.columns([3,3,3,3,3])
        overview = col1.button('Overview')
        data_visualise = col2.button('Visualise your data')
        model_analyse = col3.button('Model Analysis')
        roc = col4.button('ROC Curves')
        feature_interaction = col5.button("Feature Interaction")

        # target variable
        y = self.dataset.type
        data_pred = self.model_interpreter.predict(self.dataset.iloc[:, 0:12])
        label = self.dataset.type.unique()

        # If we click the button name then the respective mapped function will display
        if overview:
            st.title("View Data")
            st.header("This is a sample view method which will be changed in future")
            self.data()
        
        elif data_visualise:
            self.visualise()
        
        elif model_analyse:
            st.title("yet to implement")
            self.modelAnalysis(y,data_pred,label)
        
        elif roc:
            st.title("yet to implement")
        
        elif feature_interaction:
            self.featureInteraction()