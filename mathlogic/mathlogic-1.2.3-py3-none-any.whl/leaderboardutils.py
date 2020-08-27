### Set up Bascis and define functions to 
from jinja2 import Template
from IPython.core.display import display, HTML
import pandas as pd
import numpy as np
import hashlib
import mysql.connector
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

leaderboard = Template("""
<!doctype html>
<html>
  <head>
    <title>{{ title }}</title>
    <style>
        @import url("https://fonts.googleapis.com/css?family=Red+Hat+Display:400,900&display=swap");
        body, html {
          height: 100%;
          width: 100%;
        }

        .center {
          position: absolute;
          top: 50%;
          left: 50%;
          -webkit-transform: translate(-50%, -50%);
                  transform: translate(-50%, -50%);
          z-index: 10;
          font-family: 'Red Hat Display', sans-serif;
        }

        .top3 {
          display: -webkit-box;
          display: flex;
          -webkit-box-pack: center;
                  justify-content: center;
          -webkit-box-align: end;
                  align-items: flex-end;
          color: #4B4168;
        }
        .top3 .item {
          box-sizing: border-box;
          position: relative;
          background: #0080ff;
          width: 10rem;
          height: 12rem;
          text-align: center;
          padding: 2.8rem 0 0;
          margin: 1rem 1rem 2rem;
          border-radius: 0.5rem;
          -webkit-transform-origin: bottom;
                  transform-origin: bottom;
          cursor: pointer;
          -webkit-transition: -webkit-transform 200ms ease-in-out;
          transition: -webkit-transform 200ms ease-in-out;
          transition: transform 200ms ease-in-out;
          transition: transform 200ms ease-in-out, -webkit-transform 200ms ease-in-out;
          box-shadow: 0 0 4rem 0 rgba(0, 0, 0, 0.1), 0 1rem 2rem -1rem rgba(0, 0, 0, 0.3);
        }
        .top3 .item .pic {
          position: absolute;
          top: -2rem;
          left: 2.5rem;
          width: 4rem;
          height: 4rem;
          border-radius: 50%;
          background-size: cover;
          background-position: center;
          margin-right: 1rem;
          background: #ff8000;;
          box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2), 0 1rem 1rem -0.5rem rgba(0, 0, 0, 0.3);
        }
        .top3 .item .pos {
          font-weight: 900;
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
        }
        .top3 .item .name {
          font-size: 1.1rem;
          color : purple;
          margin-bottom: 0.5rem;
        }
        .top3 .item .score {
          opacity: 0.5;
          font-size: 1rem;
        }
        .top3 .item .score:after {
          display: block;
          content: '{{ post_text }}';
          opacity: 0.5;
        }
        .top3 .item.one {
          width: 10rem;
          height: 15rem;
          padding-top: 3.5rem;
        }
        .top3 .item.one .pic {
          width: 5rem;
          height: 5rem;
          left: 2.5rem;
        }
        .top3 .item:hover {
          -webkit-transform: scale(1.05);
                  transform: scale(1.05);
        }

        .list {
          padding-left: 2rem;
          margin: 0 auto;
        }
        .list .item {
          position: relative;
          display: -webkit-box;
          display: flex;
          -webkit-box-align: center;
                  align-items: center;
          background: white;
          height: 4rem;
          border-radius: 4rem;
          margin-bottom: 2rem;
          margin-right: 2rem;
          background: #0080ff;
          -webkit-transform-origin: left;
                  transform-origin: left;
          cursor: pointer;
          -webkit-transition: -webkit-transform 200ms ease-in-out;
          transition: -webkit-transform 200ms ease-in-out;
          transition: transform 200ms ease-in-out;
          transition: transform 200ms ease-in-out, -webkit-transform 200ms ease-in-out;
          box-shadow: 0 0 4rem 0 rgba(0, 0, 0, 0.1), 0 1rem 2rem -1rem rgba(0, 0, 0, 0.3);
        }
        .list .item .pos {
          font-weight: 900;
          position: absolute;
          left: -2rem;
          text-align: center;
          font-size: 1.25rem;
          width: 1.5rem;
          color: purple;
          opacity: 0.6;
          -webkit-transition: opacity 200ms ease-in-out;
          transition: opacity 200ms ease-in-out;
        }
        .list .item .pic {
          width: 4rem;
          height: 4rem;
          border-radius: 50%;
          background-size: cover;
          background-position: center;
          margin-right: 1rem;
          background-color: #ff8000;
          box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2), 0 1rem 1rem -0.5rem rgba(0, 0, 0, 0.3);
        }
        .list .item .name {
          -webkit-box-flex: 2;
                  flex-grow: 2;
          flex-basis: 10rem;
          font-size: 1.5rem;
          color : purple;
        }
        .list .item .score {
          margin-right: 1.5rem;
          opacity: 0.5;
          font-size: 1rem;
        }
        .list .item .score:after {
          margin-right: 1rem;
          content: '{{ post_text }}';
          opacity: 0.8;
        }
        .list .item:hover {
          -webkit-transform: scale(1.05);
                  transform: scale(1.05);
        }
        .list .item:hover .pos {
          opacity: 0.8;
        }

    </style>
  </head>
  <body>
    <div class="list">
              <h1 style="text-align:center">{{ title }}</h1>
    </div>
        <div class="list">
              <h1 style="text-align:center">{{ client }} : {{ phase}}</h1>
    </div>
    <div class="list">
              <h1 style="text-align:center"></h1>
    </div>
        <div class="top3"> {% for data2_records in data2 %}
            <div class="two item">
              <div class="pos">
            {{data2_records.rank}}
              </div>
              <div class="pic" style="background-image: url(&#39;{{ data2_records.img_url }}#39;)"></div>
              <div class="name">
                {{data2_records.name}}
              </div>
              <div class="score">
                {{data2_records.score}}
              </div>
            </div> {% endfor %}
            <div class="one item"> {% for data1_records in data1 %}
              <div class="pos">
                {{data1_records.rank}}
              </div>
              <div class="pic" style="background-image: url(&#39;{{ data1_records.img_url }}#39;)"></div>
              <div class="name">
                {{data1_records.name}}
              </div>
              <div class="score">
                {{data1_records.score}}
              </div>
            </div> {% endfor %}
            <div class="three item"> {% for data3_records in data3 %}
              <div class="pos">
                {{data3_records.rank}}
              </div>
              <div class="pic" style="background-image: url(&#39;{{ data3_records.img_url }}#39;)"></div>
              <div class="name">
                {{data3_records.name}}
              </div>
              <div class="score">
                {{data3_records.score}}
              </div>
            </div>  {% endfor %}
        </div>
        <div class="list">
            {% for records in data %}
             <div class="item">
              <div class="pos">
               {{ records.rank }}
              </div>
              <div class="pic" style="background-image: url(&#39;{{ records.img_url }}&#39;)"></div>
              <div class="name">
                {{records.name}}
              </div>
              <div class="score">
                {{records.score}}
              </div>
            </div>
          {% endfor %}
        </div>
  </body>
</html>
""")

def get_leaderboard(eventid,client,phase,return_format='dataframe',level="team"):
    if level=="team":
        leaderboard_query = "select eventid,client,phase,team as user,round(max(score),3) as max_score, round(min(score),3) as min_score, max(email) as email,team as team, max(score_sort) as score_sort, max(metric) as metric,count(*) as submissions  from mdl_hack_score where eventid = '{}' and client = '{}' and phase = '{}' and exclude is Null group by eventid, client, team, phase".format(eventid,client,phase)
    else:
        leaderboard_query = "select eventid,client,phase,user,round(max(score),3) as max_score, round(min(score),3) as min_score, max(email) as email,max(team) as team, max(score_sort) as score_sort, max(metric) as metric,count(*) as submissions  from mdl_hack_score where eventid = '{}' and client = '{}' and phase = '{}' and exclude is Null group by eventid, client, user, phase".format(eventid,client,phase)
    try:
        mydb = mysql.connector.connect(host="www.fnmathlogic.com",user="mlportal_hack", password="m@thhackathon", database="mlportal_mdln1")
        mycursor = mydb.cursor()
        mycursor.execute(leaderboard_query)
        df=pd.DataFrame(mycursor.fetchall(),columns=["eventid","client","phase","user","max_score","min_score","email","team","score_sort","metric","submissions"])
        mydb.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return "1","Something went wrong: {}".format(err)

    #df=pd.DataFrame(mycursor.fetchall(),columns=["id","eventid","client","phase","user","score","timechar","score_sort","metric","exclude","team","email","sys_time"])
    if df.shape[0]< 4:
        if df.shape[0]==0:
            sort_order = 1
            metric = ""
        else:
            sort_order = df.iloc[0,8]
            metric = df.iloc[0,9]
        df2 = pd.DataFrame({"min_score":[1000000,1000000,1000000,1000000],"max_score":[0,0,0,0],"user":["yet.to.submit","yet.to.submit","yet.to.submit","yet.to.submit"],"client":["mathlogic","mathlogic","mathlogic","mathlogic"]})
        df=df.append(df2[:4-df.shape[0]],ignore_index=True)
    else:
        sort_order = df.iloc[0,8]
        metric = df.iloc[0,9]
    if sort_order == 0:
        df.rename(columns={'max_score':'score'},inplace=True)
        sort_bool=False
    else:
        df.rename(columns={'min_score':'score'},inplace=True)
        sort_bool=True

    df.sort_values(by='score',ascending=sort_bool,inplace=True)
    df.reset_index(inplace=True,drop=True)
    df['rank']=df.index+1

    df['email']= df.apply(lambda x: x['user']+"@"+x['client']+".com" if x['email'] in [None,'',np.NaN] else x['email'],axis=1)
    df['img_url']=df.apply(lambda x: "https://www.gravatar.com/avatar/"+hashlib.md5((x['email']).encode()).hexdigest()+"?d=robohash",axis=1)
    df['name'] = df.apply(lambda x: ".".join([y.capitalize() for y in x['user'].split('@')[0].split(".")]),axis=1)
    data1 = df.iloc[[0]].to_dict('records')
    data2 = df.iloc[[1]].to_dict('records')
    data3 = df.iloc[[2]].to_dict('records')
    data = df.iloc[3:].to_dict('records')
    leaderboard_html = leaderboard.render(data1=data1,data2=data2,data3=data3,data=data,post_text=metric,client=client.upper(), phase=phase.capitalize(), title="Hackathon Leaderboard") 

    if return_format == 'dataframe':
        #print(df)
        return df[df['user'] != 'yet.to.submit'][["rank","user","team","score","submissions"]]
    elif return_format == 'html':
        #print(leaderboard_html)
        return leaderboard_html
    elif return_format == "display_html":
        from IPython.core.display import display, HTML
        display(HTML(leaderboard_html))
        return None
    

