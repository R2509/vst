git add .
git commit -nm bruh
git push

echo "exit workspace?"
read ws
if ws == "y" or ws == "yes" then
    gp stop
fi;

echo "exit this terminal?"
read ws
if $ws == "y" or $ws == "yes" then
    exit
fi;