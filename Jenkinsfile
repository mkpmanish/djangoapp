pipeline {
    agent none
    stages {
	stage('-Build App'){
		agent any
	 	//environment {
        	//	MY_CREDENTIALS = credentials('6ef6ab6d-4f21-46d1-a173-e97f829e294c')
    		//}

		steps {
			git(
        		        url:  'git@github.com:mkpmanish/djangoapp.git',
             			   branch: 'dev',
               			 changelog: true,
               			credentialsId: '6ef6ab6d-4f21-46d1-a173-e97f829e294c'
				 poll: true
                	)
			sh 'grep -ri 8888 *'
			sh 'uname -a'
			sh 'hostname'
			sh 'docker build -t myhellopy .'
			sh 'docker run -p 8800:8800 -d myhellopy'
			sh 'sleep 10'
			sh 'curl http://$(curl http://checkip.amazonaws.com):8800/'
		  	sh 'cat ./Jenkinsfile'
			//echo "username is $MY_CREDENTIALS_USR"
		}
	}


 
        stage("Run SAST - Bandit"){
                agent any
                steps { script{
                   try{
                        echo "Runing SCA scan..........."
                        //sh 'docker run --rm --volume /var/lib/jenkins/workspace/NS-GITHUB-JENKINS:/src:rw secfigo/bandit:latest'
                        sh 'docker run --rm --volume /var/lib/jenkins/workspace/NS-GITHUB-JENKINS:/src:rw secfigo/bandit:latest > output.txt'
               } catch(Exception e){
                        echo "Bandit Scan failed for some reason...." + e.getMessage()
                }}
           }
        }

	stage("Run Merge"){
                agent any
                steps { script{
                   try{
			sh 'cat ./checkstatus.sh'
                        echo "Runing Checks if High is present or not..........."
                        sh 'chmod +x checkstatus.sh && ./checkstatus.sh'
                   } catch(Exception e){
                        echo "Bandit Scan failed for some reason...." + e.getMessage()
                }
	     }
           }
        }


	stage('Post-Merge Actions') {
            steps {
                script {
                    def comment = 'Build result: ' + currentBuild.result.toString()
                    // Additional logic for comment content
                    pullRequest comment(body: comment)
                }
            }
        }


	stage("Cleanup"){
		agent any
		steps{
			sh 'if [ $(docker ps | awk \'{print $1}\' | tail -1) ];then docker stop $(docker ps | awk \'{print $1}\' | tail -1);fi'
		}
	}
    }
}
