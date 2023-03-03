from flask import Flask, request, session, redirect, render_template
import os,openai
# create the flask app
app = Flask(__name__)
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'
openai.api_key = "api_key"


def generate_text(messages):

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )

    output = response.choices[0].message.content.strip()

    return output

@app.route('/logout')
def logout():
   session.pop('data', None)
   return redirect('http://url/')

@app.route('/', methods=['GET','POST'])
def chat():
    
    if 'data' in session:

        messages = session['data']
        if request.method == 'POST':  
            # get the description submitted on the web page
            prompt = request.form.get('description')
            if len(prompt)>0:
                session['data'].append({"role": "user", "content": prompt},)
                
                messages = session['data']
                a_description = generate_text(messages)
                
                messages.append({"role": "assistant", "content": a_description},)
                session['data'] = messages
        
    else:
        session['data'] = [{"role": "system", "content": "You are a helpful assistant."},]
    
    return render_template('app_frontend.html', data = session['data'])


# boilerplate flask app code
if __name__ == "__main__":
    port = int(os.environ.get('PORT',80))
    app.run(debug=True, host='0.0.0.0', port=port)
