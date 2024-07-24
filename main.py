from authentification import authentificate
import posting as ps

driver = authentificate(
    "https://hootsuite.com/dashboard", "achrafchahbon5@gmail.com", "Achraf@123mary"
)
ps.Posting(
    driver,
    "#fyp #fypシ #brawlstarstiktok #brawlstars #new #battlepass",
    r"C:\Users\kinga\Desktop\project\'autoLoader\video_creator\stars.mp4",
    iteration=6
)

