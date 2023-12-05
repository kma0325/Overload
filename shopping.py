from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

#애플리케이션 객체 생성
app = Flask(__name__) 

#MySQL 연결설정
mysql = MySQL(app) 
app.config['MYSQL_HOST'] = '158.247.230.44'  # MySQL 서버 주소
app.config['MYSQL_USER'] = 'dev'  # MySQL 사용자 이름
app.config['MYSQL_PASSWORD'] = 'overload'  # MySQL 비밀번호
app.config['MYSQL_DB'] = 'userinfo'  # 사용할 데이터베이스 이름

#회원가입 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        nickname = request.form['nickname']
        email = request.form['email']

        try:
            #mysql과 상호작용하는 커서 객체 생성
            cur = mysql.connection.cursor()

            cur.execute("SELECT * FROM user WHERE id = %s OR email = %s", (userid, email))
            existing_user = cur.fetchone()

            if existing_user:
                error_message = '이미 존재하는 아이디 또는 이메일입니다.'
                return render_template('register.html', error_message=error_message)
            
            #SQL 쿼리 실행
            cur.execute("INSERT INTO user (id, name, pw, email) VALUES (%s, %s, %s, %s)",
                    (userid, password, nickname, email))

            #변경 사항을 확정시킴(반드시 호출되어야 함)
            mysql.connection.commit()

            #커서를 닫아줌
            cur.close()
        
        except Exception as e:
            return f'에러 발생: {str(e)}'

    return render_template('register.html')

#문의 글을 담을 리스트
inquiries = []

#문의 글을 제출하는 페이지 라우팅
@app.route('/submit_inquiry')
def submit_inquiry():
    return render_template('submit_inquiry.html')

@app.route('/submit_inquiry', methods=['POST'])
#문의 글을 제출하는 기능 
def submit():
    username = request.form.get('username')
    inquiry_text = request.form.get('inquiry_text')

    if username and inquiry_text:
        inquiries.append({'username': username, 'inquiry_text': inquiry_text})
    
    return render_template('submit_inquiry.html')

#문의 글을 볼 수 있는 페이지 라우팅
@app.route('/inquiry')
def reviews():
    return render_template('inquiry.html', inquiries=inquiries)

if __name__ == '__main__':
    app.run(debug=True)