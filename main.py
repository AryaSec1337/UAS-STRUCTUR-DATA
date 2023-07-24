import pandas as pd
from googleapiclient.discovery import build

def video_comments(video_id):
	# empty list for storing reply
	replies = []

	# creating youtube resource object
	youtube = build('youtube', 'v3', developerKey=api_key)

	# retrieve youtube video results
	video_response = youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()

	# iterate video response
	while video_response:

		# extracting required info
		# from each result object
		for item in video_response['items']:

			# Extracting comments ()
			published = item['snippet']['topLevelComment']['snippet']['publishedAt']
			user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']

			# Extracting comments
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']

			replies.append([published, user, comment, likeCount])

			# counting number of reply of comment
			replycount = item['snippet']['totalReplyCount']

			# if reply is there
			if replycount>0:
				# iterate through all reply
				for reply in item['replies']['comments']:

					# Extract reply
					published = reply['snippet']['publishedAt']
					user = reply['snippet']['authorDisplayName']
					repl = reply['snippet']['textDisplay']
					likeCount = reply['snippet']['likeCount']

					# Store reply is list
					#replies.append(reply)
					replies.append([published, user, repl, likeCount])

			# print comment with list of reply
			#print(comment, replies, end = '\n\n')

			# empty reply list
			#replies = []

		# Again repeat
		if 'nextPageToken' in video_response:
			video_response = youtube.commentThreads().list(
					part = 'snippet,replies',
					pageToken = video_response['nextPageToken'],
					videoId = video_id
				).execute()
		else:
			break
	#endwhile
	return replies
# isikan dengan api key Anda
api_key = 'AIzaSyCAb1ENkMlWrykJv63YB5ONUVHE6y96hL0'

video_id = input("masukan ID youtube: ")

# Call function
comments = video_comments(video_id)

comments

df = pd.DataFrame(comments, columns=['publishedAt', 'authorDisplayName', 'textDisplay', 'likeCount'])
df

df.to_csv('youtube-comments.csv', index=False)


import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt

# Membaca file CSV dan membersihkan data
file_path = input("Masukan file berbentuk CSV!: ")
df = pd.read_csv(file_path)
df['textDisplay'] = df['textDisplay'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))

# Membaca kata kunci dari pengguna
keywords = input("Masukkan keyword (pisahkan dengan koma): ").split(',')

# Meminta jumlah maksimum kata kunci yang ingin digunakan
max_keywords = int(input("Masukkan jumlah maksimum keyword yang ingin digunakan: "))

# Memastikan jumlah kata kunci tidak melebihi batasan
keywords = keywords[:max_keywords]

# Membuat objek Graph
G = nx.Graph()

# Menambahkan node presiden
G.add_node('presiden')

# Menambahkan node sesuai kata kunci
for keyword in keywords:
    G.add_node(keyword.strip())

# Menambahkan edge antara presiden dengan node sesuai kata kunci
for keyword in keywords:
    G.add_edge('presiden', keyword.strip())

# Menambahkan data pengguna ke node yang sesuai
keyword_data = {}

for index, row in df.iterrows():
    authorDisplayName = row['authorDisplayName']
    textDisplay= row['textDisplay']

    for keyword in keywords:
        if keyword.strip().lower() in textDisplay.lower():
            G.add_edge(keyword.strip(), authorDisplayName) 

# Simpan dataset yang telah disaring berdasarkan semua keyword ke dalam file CSV baru
filtered_df = df[df['textDisplay'].str.contains('|'.join(keywords), case=False)]
filtered_df.to_csv('data_filtered_youtube.csv', index=False)

print("Dataset yang telah disaring telah disimpan dalam file:")

# Menampilkan grafik menggunakan NetworkX dan matplotlib
pos = nx.spring_layout(G, seed=42)  # Set a seed for reproducibility
plt.figure(figsize=(2, 7))
nx.draw(G, pos, with_labels=False, node_color='orange', edge_color='green', font_size=12, font_weight='bold')
plt.title('Social Network Analysis (SNA) Graph')
plt.show()

# Membuat Bar Chart
plt.figure(figsize=(10, 5))
keyword_counts = filtered_df['authorDisplayName'].value_counts()

# Membuat plot bar chart
bars = plt.bar(keyword_counts.index, keyword_counts.values, color=plt.cm.Paired.colors)

# Menambahkan label pada tiap bar
for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), bar.get_height(), ha='center', va='bottom')

plt.xlabel('Author Display Name')
plt.ylabel('Count')
plt.title('Top Authors Based on Keyword Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Membuat Pie Chart
plt.figure(figsize=(7, 7))
keyword_percentages = keyword_counts / keyword_counts.sum() * 100

# Membuat plot pie chart
wedges, texts, autotexts = plt.pie(keyword_percentages, labels=keyword_percentages.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)

# Menambahkan label persentase pada tiap wedge (potongan pie)
for autotext in autotexts:
    autotext.set_fontsize(12)

plt.axis('equal')
plt.title('Percentage of Top Authors Based on Keyword Frequency')
plt.tight_layout()
plt.show()

# Menghitung jumlah komentar yang mengandung masing-masing keyword
keyword_counts = {}
for keyword in keywords:
    keyword_counts[keyword.strip()] = df['textDisplay'].str.contains(keyword.strip(), case=False).sum()

# Membuat plot pie chart
plt.figure(figsize=(7, 7))
labels = list(keyword_counts.keys())
sizes = list(keyword_counts.values())

# Daftar warna sesuai dengan jumlah keyword yang berbeda
colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

plt.axis('equal')
plt.title('Jumlah Komentar Berdasarkan Keyword')
plt.tight_layout()
plt.show()
