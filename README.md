# Kiite-me!（学部密着型の就活相談サイト） 
<h4>ENG is below Japanese</h4>

# Description

<h3>【概要】</h3>
<p>　母校の大学生が同じ学部の先輩や卒業生に知恵袋サイトのような感覚で就活や学校生活の質問ができるサイト</p>

<h3>【背景・課題】</h3>
<p>　●母校の大学のキャリアセンターではOB・OG訪問をしたい場合に電話でしか繋がる方法がなかったために、敷居の高さを感じる人がいた</p>

<p>　●コロナ過でキャリアセンターが使用不可となり、上記のOB・OG訪問の連絡先の入手や、就活を終えた4年生の先輩に就活相談をする機会がなくなってしまった</p>

<p>　●私の出身学部は2016年創立であることから、2021年3月時点で1学年分しか卒業生がおらず、OB・OGの総数がそもそも少ないため、在学生にとっての「直接の先輩」に就活の相談ができる環境が必要となっていた</p>

<h3>【課題に対しての解決方法】</h3>
<p>　●知恵袋サイト感覚でざっくばらんに相談できるサイトを作成することで、これまでよりも気軽にOB・OGに就活などの相談ができる</p>

<p>　●加えて「大学全体」ではなく「学部」に初動範囲を狭めることで、前提知識が共有された人たちと繋がっている安心感を与えることができる</p>

<p>　●学部の職員と連携をとり、学部内への周知をポータルサイトで行っていただくことで在学生の参加を促す（3/15現在調整中）</p>

<h3>【今後の課題】</h3>
<p>　●在学生からの質問に答えてくれる卒業生が協力してくれるようなインセンティブの整備</p>

<h3>【今後の展望】</h3>
<p>　●規模の拡大</p>
<p>　　→ 初動は対象学部だけのサービスとしてサービスの質の向上を目指し、徐々に他学部向けにもサービスの展開を進めていきたい</p>

<p>　●就活支援サービスの充実</p>
<p>　　→ オンラインでの模擬面接や質問会などのイベントを開催し、その場でしか聞けないようなことを気軽に相談できる機会を設けたい</p>

<p>　●スポンサーの獲得</p>
<p>　　→ 現在は無償のサービスとなっているものの、今後の規模拡大を目指す際には費用も増えると仮定する。そのためこの活動に協賛していただける企業や団体を見つけたい</p>

# DEMO

<p>本番環境：https://kiite-me.site</p>

大変恐縮ではございますが、上記本番環境では学習院大学生のみに登録を限定させていただいております。

下記のデモ環境にて同様のサイトをご用意しておりますのでご参照ください。

<p>デモ環境：http://18.177.150.91:8000 （ログイン画面でのパスワードはすでに入力しております。）</p>

# Features

<h3>【環境一覧】</h3>
<p>言語　　　　　：Python</p>
<p>フレームワーク：Django</p>
<p>JSライブラリ　：Croppperjs（プロフィール画像のトリミング）</p>
<p>データベース　：PostgreSQL</p>
<p>インフラ　　　：AWS （VPC, EC2, S3, Route53）</p>
<p>Webサーバー 　：NginX</p>

<p>ドメイン取得　：お名前ドットコム</p>
<p>SSL照明書　 　：Let's Encrypt (Certbot)</p>

<p>計測ツール　　：Google Anaytics 4</p>

# Requirement

- asgiref==3.3.1
- boto3==1.16.51
- botocore==1.19.51
- bottle==0.12.19
- bottle-websocket==0.2.9
- certifi==2020.12.5
- chardet==4.0.0
- Django==3.1.4
- django-filter==2.4.0
- django-storages==1.11.1
- Eel==0.12.4
- future==0.18.2
- gevent==21.1.0
- gevent-websocket==0.10.1
- greenlet==1.0.0
- httplib2==0.18.1
- idna==2.10
- jmespath==0.10.0
- oauthlib==3.1.0
- opencv-python==4.4.0.46
- Pillow==7.2.0
- psycopg2==2.8.6
- python-dateutil==2.8.1
- pytz==2020.5
- requests==2.25.1
- requests-oauthlib==1.3.0
- s3transfer==0.3.3
- six==1.15.0
- sqlparse==0.4.1
- urllib3==1.26.2
- uWSGI==2.0.19.1
- whichcraft==0.6.1
- whitenoise==5.2.0
- zope.event==4.5.0
- zope.interface==5.2.0


# Installation

```bash
pip install -r requirements.txt
```

# Usage

```bash
git clone https://github.com/SDTakeuchi/kiitePRJCT.git
cd kiitePRJCT
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

# Author

作成者 : 武内修平 / [Douglas Shuhei Takeuchi](https://github.com/SDTakeuchi)
<p>キイテミ運営事務局 代表</p>

# License

Kiite-me! is released under [MIT license](https://en.wikipedia.org/wiki/MIT_License), see LICENSE.txt.


## Eng ver.

# Description
### "Kiite-me!" provides an opportunity for graduates to interact with alumni. The graduates can ask whatever about their job hunting, and school life, and so on.

<h3>What to solve</h3>
<p>　●Not a few graduates tend to feel hesitant to contact alumni under the system provided by University</p>

<p>　●With Covid-19 changing the graduates' environment, it has become even more difficult for them to connect senior students and alumni to ask about their experience in getting their job.</p>

<p>　●Especially the faculty I graduated from is just 5-year-old, meaning there are quite a few alumni from the faculty, which makes it even harder for graduates in the faculty to connect their own alumni.</p>

<h3>How to solve</h3>
<p>　●Making a website like Yahoo Answers, where the graduates feel relatively comfortable to ask about their job hunting.</p>

<p>　●Limiting the community within the faculty I graduated from so that the graduates feel laid back by sharing the same backgrounds.</p>

<p>　●Releasing "Kiite-me!" with communicating with the university staff, which potentially enhances the website's reliability. (the process is ongoing at the time of15th, MAR)</p>

<h3>What to consider</h3>
<p>　●The issue we are going to tackle presumably is how to incentive the cooperation by the alumni.</p>

<h3>What we want to do</h3>
<p>　●Expand the service</p>
<p>　　→ We limit the service within the faculty for the beginning to improve our websites' primary functions. Afterward, we want to expand the service to other faculties and hopefully other universities to help more students.</p>

<p>　●Holding online events</p>
<p>　　→ We want to hold online meetings where the graduates can ask the alumni in person and actively.</p>

<p>　●Inviting sponsors</p>
<p>　　→ Expanding our service across faculties, we assume that the budget will rise to some extent. To continue to provide our service, we will have to ask some company or groups to sponsor us in the future.</p>

# DEMO

<p>Actual site：https://kiite-me.site</p>
Please DO NOT sign up, since this service is limited to the Gakushuin University's students for the time being.

Please check out the demo site below instead, thank you.

<p>Demo ver.：ttp://18.177.150.91:8000 （Authentication is disabled, you can walk around the website.）</p>

# Features

<p>Python / Django</p>
<p>Cropperjs for avater image edit</p>
<p>PostgreSQL</p>
<p>AWS （VPC, EC2, S3, Route53）</p>
<p>NginX</p>
<p>Google Anaytics 4</p>


# Requirement

- asgiref==3.3.1
- boto3==1.16.51
- botocore==1.19.51
- bottle==0.12.19
- bottle-websocket==0.2.9
- certifi==2020.12.5
- chardet==4.0.0
- Django==3.1.4
- django-filter==2.4.0
- django-storages==1.11.1
- Eel==0.12.4
- future==0.18.2
- gevent==21.1.0
- gevent-websocket==0.10.1
- greenlet==1.0.0
- httplib2==0.18.1
- idna==2.10
- jmespath==0.10.0
- oauthlib==3.1.0
- opencv-python==4.4.0.46
- Pillow==7.2.0
- psycopg2==2.8.6
- python-dateutil==2.8.1
- pytz==2020.5
- requests==2.25.1
- requests-oauthlib==1.3.0
- s3transfer==0.3.3
- six==1.15.0
- sqlparse==0.4.1
- urllib3==1.26.2
- uWSGI==2.0.19.1
- whichcraft==0.6.1
- whitenoise==5.2.0
- zope.event==4.5.0
- zope.interface==5.2.0


# Installation

```bash
pip install -r requirements.txt
```

# Usage

```bash
git clone https://github.com/SDTakeuchi/kiitePRJCT.git
cd kiitePRJCT
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

# Author

武内修平(Legal Name) / [Douglas Shuhei Takeuchi](https://github.com/SDTakeuchi)
<p>Representative of Kiite-me! Management Office</p>

# License

Kiite-me! is released under [MIT license](https://en.wikipedia.org/wiki/MIT_License), see LICENSE.txt.