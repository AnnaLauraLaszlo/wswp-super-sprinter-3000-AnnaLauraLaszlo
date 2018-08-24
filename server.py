from flask import Flask, request, render_template, session, redirect
import common


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_index():
    datatable = common.get_table_from_file('data.csv')
    return render_template('list.html', datatable= datatable)


@app.route('/story')
def route_story():
    return render_template('form.html')


@app.route('/save_story', methods=['POST'])
def route_save_story():
    table = common.get_table_from_file('data.csv')
    if request.method == 'POST':
        story_title = request.form['story_title']
        user_story = request.form['user_story']
        acceptance_criteria = request.form['acceptance_criteria']
        business_value = str(request.form['business_value']) + ' points'
        estimation = str(request.form['estimation']) + ' h'
        new_id = str(int(table[-1][0]) + 1)
        new_story_list = [new_id, story_title, user_story, acceptance_criteria, business_value, estimation, 'planning']
        table.append(new_story_list)
        common.write_table_to_file('data.csv', table)
    return redirect('/')


@app.route('/story/<int:story_id>')
def route_update_story(story_id):
    table = common.get_table_from_file('data.csv')
    for line in table:
        if line[0] == str(story_id):
            story_title = line[1]
            user_story = line[2]
            acceptance_criteria = line[3]
            business_value = line[4].split()
            business_value = int(business_value[0])
            estimation = line[5].split()
            estimation = float(estimation[0])
            status = line[6]

            return render_template('update.html', story_id= story_id, story_title= story_title, user_story= user_story,
                                   acceptance_criteria= acceptance_criteria, business_value= business_value,
                                   estimation= estimation, status= status)


@app.route('/save_updated_story/<story_id>', methods=['POST'])
def route_save_updated_story(story_id):
    table = common.get_table_from_file('data.csv')
    if request.method == 'POST':
        story_title = request.form['story_title']
        user_story = request.form['user_story']
        acceptance_criteria = request.form['acceptance_criteria']
        business_value = str(request.form['business_value']) + ' points'
        estimation = str(request.form['estimation']) + ' h'
        status = request.form['status']
        for line in table:
            if line[0] == str(story_id):
                line.clear()
                updated_story_list = [story_id, story_title, user_story, acceptance_criteria, business_value, estimation, status]
                for i in updated_story_list:
                    line.append(i)
                common.write_table_to_file('data.csv', table)
                return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug= True, port= 5000)