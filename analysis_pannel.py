# code to run a App in web showing a bar graph which simulates the fill level of each smart bin
import pandas as pd
import dash
import plotly.express as px
import firebase_admin
from firebase_admin import credentials, db # for Firestore
from dash import dcc, html, Input, Output

def determine_bar_color(value):
            if value > 30:
                return 'red'
            else:
                return 'blue'
# providing the credentials of the Firebase
cred = credentials.Certificate('D:\jamu\Hackathon\smartbin-data-firebase-adminsdk-rbe43-5c744321e5.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartbin-data-default-rtdb.firebaseio.com/'
})
# running the dash app
app = dash.Dash(__name__)

#------------------------------------------------------------------------
app.layout = html.Div([
     html.H1("Smartbin Supervision Pannel", style={'text-align': 'center'}),
    dcc.Interval(
                id='my_interval',
                disabled=False,     #if True, the counter will no longer update
                interval=1*5000,    #increment the counter n_intervals every interval milliseconds
                n_intervals=0,      #number of times the interval has passed
                max_intervals=-1,   #number of times the interval will be fired.
                                    #if -1, then the interval has no limit (the default)
                                    #and if 0 then the interval stops running.
    ),

    dcc.Graph(id="mybarchart"),

])

#------------------------------------------------------------------------
@app.callback(
    [Output('mybarchart', 'figure')],
    [Input('my_interval', 'n_intervals')]
)
def update_graph(num):
        """update every 5 seconds"""
        ref = db.reference('S-001')
        data = ref.get()
        capacity=30
        # creating a dictionary of values which contains smart-bin id and fill-up value(ie. capacity minus distance) and Time
        data_dict=[{'id':'S001','Distance':round(capacity-data['Distance'],2),'Time':data['Time']}]
        # for multiple machines considering data
        data_dict.append({'id':'S002','Distance':13.13,'Time':'203-08-14T09:26:08.085201'})
        data_dict.append({'id':'S003','Distance':33.12,'Time':'203-08-14T09:26:08.085201'})
        data_dict.append({'id':'S004','Distance':0.23,'Time':'203-08-14T09:26:08.085201'})
        data_dict.append({'id':'S005','Distance':10.3,'Time':'203-08-14T09:26:08.085201'})
        df=pd.DataFrame(data_dict)
        # plotting a bar graph
        fig=px.bar(df, x='id', y='Distance', title='Distance vs. ID',color='Distance',
                      color_discrete_map={value: determine_bar_color(value) for value in df['Distance']})
        return [fig]

if __name__ == '__main__':
    app.run_server(debug=True)

# This simulation represents the fill-level of one Smart-Bin, further multiple Smart-Bin values can be simulated following the same procedure as that of Smart-bin S001
