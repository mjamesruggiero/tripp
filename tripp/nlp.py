import matplotlib.pyplot as pyplot

data = [
    ("big data", 100, 15),
    ("hadoop", 95, 25),
    ("python", 75, 50),
    ("R", 50, 40),
    ("machine learning", 80, 20),
    ("statistics", 20, 60),
    ("data science", 60, 70),
    ("analytics", 90, 3),
    ("team player", 85, 85),
    ("dynamic", 2, 90),
    ("synergies", 70, 0),
    ("actionable insights", 40, 30),
    ("self-starter", 30, 50),
    ("think out of the box", 45, 10),
    ("customer focus", 65, 15),
    ("thought leadership", 35, 35)
]


def text_size(total):
    """Equals 8 if total is 0, 28 if total is 200"""
    return 8 + total / 200 * 20

if __name__ == '__main__':
    for word, job_popularity, resume_popularity in data:
        pyplot.text(job_popularity, resume_popularity, word,
                 ha='center', va='center',
                 size=text_size(job_popularity + resume_popularity))
    pyplot.xlabel("Popularity of jobs postings")
    pyplot.ylabel("Popularity on resumes")
    pyplot.axis([0, 100, 0 , 100])
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.show()
