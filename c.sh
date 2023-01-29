git add .
git commit -nm bruh
git push

echo "exit workspace?"
read

if ["$REPLY" = "y" or "$REPLY" = "yes"]; then
    gp stop;
fi

echo "exit this terminal?"
read
if ["$REPLY" = "y" or "$REPLY" = "yes"]; then
    exit;
fi