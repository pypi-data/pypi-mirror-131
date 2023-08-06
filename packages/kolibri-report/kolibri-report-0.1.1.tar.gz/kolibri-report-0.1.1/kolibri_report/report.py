from abc import ABC,abstractclassmethod
import streamlit as st
import seaborn as sns
import json,os

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
    def __init__(self,data=None,model_interpreter=None,model_directory=None) -> None:
        """A constructor which takes the data, model_interpreter and the trainer as important parameter and 

        Args:
            data (Dataframe, optional): Pandas Dataframe(Dataset). Defaults to None.
            model_interpreter (ModelLoader, optional) : A model loader where we fetch all the training and test data Defaults to None.
            model_directory (String, optional): Directory path to fetch metetajson file. Defaults to None.
        """
        self.dataset = data
        self.model_directory = model_directory
        self.model_interpreter = model_interpreter

    def getInformation(self):
        """Reads the metajson file and fetches all the information required for the Overview tab.

        Returns:
            tuple[int | Date]: Returns kolibri version and date at which it executed
        """
        from datetime import datetime
        for i in os.listdir(self.model_directory):
            if '.json' in i:
                fileOpen = self.model_directory+'/'+i
                f = open(fileOpen,'r')
                data = json.load(f)
                kolibri_version = data['kolibri_version']
                trained_at,time_trained = data['trained_at'].split('-')
                time_finished = ":".join([time_trained[i:i+2] for i in range(0, len(time_trained), 2)])
                date = datetime.strptime(trained_at,'%Y%m%d').strftime('%d/%m/%Y')
        return kolibri_version,date,time_finished
    
    def data(self):
        '''
        This method displays description of the model, Model Version​,Kolibri Version​,Owner​ and Trained at​.
        '''
        train_time,date,time_finished = self.getInformation()
        st.header(f'Kolibri Version used is {train_time}')
        st.header(f'Date completed {date} at {time_finished}')
        st.table(self.dataset[:5])
    
    
    def visualise(self):
        for i in os.listdir(self.model_directory):
            if '.json' in i:
                fileOpen = self.model_directory+'/'+i
                f = open(fileOpen,'r')
                data = json.load(f)
                target = data['pipeline'][-1]['fixed']['target']
        st.title('Visualising our dataset!!')
        # if we choose the options we get our output result as list
        col1,col2 = st.columns([2,2])
        with col1:
            st.write(''' #### Class comparison for our dataset''')
            sns.countplot(x=target,data=self.dataset)
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
        with col2:
            st.write(''' #### Heatmap for our dataset''')
            sns.heatmap(self.dataset.corr(),cmap='Greens')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""The chart above shows some numbers class present in our dataset.""")
    
    
    def fetchScores(self):
        """A method which fetch all the scores from the metajson file and plots all the result.

        Returns:
            tuple[Unbound | DataFrame, Unbound | DataFrame, Unbound | DataFrame, Unbound | Series]: Returns cf_matrix and all scores
        """
        import json,os,pandas as pd
        for i in os.listdir(self.model_directory):
            if '.json' in i:
                fileOpen = self.model_directory+'/'+i
                f = open(fileOpen,'r')
                data = json.load(f)
                dict_val = [i for i in data['pipeline'] if 'performace_scores' in i][0]
                confussionMatrix = pd.DataFrame(dict_val['performace_scores']['confusion_matrix'])
                class_report = pd.DataFrame(dict_val['performace_scores']['class_report'])
                class_report.drop(class_report.index[len(class_report)-1],inplace=True) # Droping support
                new_class_report = class_report.iloc[: ,0:2]
                score_report = class_report.iloc[:, 2:]
                res_score = dict([(k,dict_val['performace_scores'][k]) for k in dict_val['performace_scores'].keys() if k not in ['confusion_matrix', 'class_report']])
                res_score = pd.Series(res_score)
        return confussionMatrix,new_class_report,score_report,res_score
                
    def modelAnalysis(self):
        """This is a function where it plots all the score analysis such as precision,recall,f1-score and 
        accuracy.
        """
        import numpy as np
        confussionMatrix,class_report,score_report,res_score = self.fetchScores()
        col1,col2= st.columns(2)
        with col1:
            st.write(''' #### Confusion Matix for our dataset''')
            sns.heatmap(confussionMatrix/np.sum(confussionMatrix), annot=True, fmt='.2%')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""A random text about confusion matrix""")
        
        with col2:
            st.write(''' #### Class Reprot for our dataset''')
            ax = class_report.plot(kind='bar')
            for p in ax.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                ax.annotate(f'{height:.0%}', (round(x + width/2,2), round(y + height*1.02,2)), ha='center')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""A random text about confusion matrix""")
        # st.write(score_report,'\n',res_score)

        col3,col4= st.columns(2)
        with col3:
            st.write(''' #### Accuracy,Macro Average and Weighted Average for our dataset''')
            ax1 = res_score.plot(kind='bar', color=['black', 'red', 'green', 'blue', 'coral','limegreen','darkkhaki','thistle','chocolate','peru','darkgoldenrod','steelblue'])
            for p in ax1.patches:
                width1 = p.get_width()
                height1 = p.get_height()
                x1, y1 = p.get_xy() 
                ax1.annotate(f'{height1:.0%}', (round(x1 + width1/2,2), round(y1 + height1*1.02,2)), ha='center')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""A random text about confusion matrix""")
    
    def featureInteraction(self):
        """Checking our feature how it interacts with other feature. We provde you a dropbox 
        functionality and then you can analyse the interactn fo the features.
        """
        pass

    
    def run(self):
        st.page_config = st.set_page_config(
            page_title="Kolibri report",
            layout="wide",
        )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        col1,col2,col3,col4,col5 = st.columns([3,3,3,3,3])
        overview = col1.button('Overview')
        data_visualise = col2.button('Visualise your data')
        model_analyse = col3.button('Model Analysis')
        roc = col4.button('ROC Curves')
        feature_interaction = col5.button("Feature Interaction")

        # If we click the button name then the respective mapped function will display
        if overview:
            st.title("A detailed overview of our model")
            self.data()
        
        elif data_visualise:
            self.visualise()
        
        elif model_analyse:
            self.modelAnalysis()
        
        elif roc:
            st.title("yet to implement")
        
        elif feature_interaction:
            st.title('Feature Interactions for our datset!!')
            st.header('Upcoming feature')