from authentification import authentificate
import posting as ps

driver = authentificate(
    "https://hootsuite.com/dashboard", "achrafchahbon5@gmail.com", "Achraf@123mary"
)
ps.Posting(
    driver,
    "the best video in the world",
    r"C:\Users\kinga\Desktop\project\'autoLoader\video_creator\video\stars_part3.mp4",
    iteration=5
)

