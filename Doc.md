#GIT HUB  

…or create a new repository on the command line
echo "# online-library" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/rco-architect/online-library.git
git push -u origin main

 


…or push an existing repository from the command line
 git remote add origin https://github.com/rco-architect/online-library.git
git branch -M main
git push -u origin main



Clone
git clone https://github.com/rco-architect/online-library.git
cd online-library

```
online-library/
├── index.html                   # Book library catalog
├── README.md
├── .gitignore
│
├── public/                      # Public site assets (favicons, book cover images)
│   └── covers/
│       ├── book1-cover.png
│       └── book2-cover.png
│
└── src/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    └── pages/
        └── reader.html          # PDF reader page
```

