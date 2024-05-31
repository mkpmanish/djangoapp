var=$(cat /var/lib/jenkins/workspace/NS-GITHUB-JENKINS/output.txt  | grep "Medium"  | awk '{print $2}' | tail -1)
#var=$(cat ./output.txt  | grep "High"  | awk '{print $2}' | tail -1)


echo $var
if [ "$var" -gt "0" ]
then
	echo "High Vulnerability Found"
	exit 1
else
	echo "No High Found"
	exit 0
fi
