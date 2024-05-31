pipeline {
    agent any


    stages {

	stage("Pre-Runup-Cleanup"){
                agent any
                steps{ script{ try {
                        sh 'if [ $(docker ps | awk \'{print $1}\' | tail -1) ];then docker stop $(docker ps | awk \'{print $1}\' | tail -1);fi'
                }catch(Exception e){
			echo "No Docker lying around so no cleanup"	
		}
	      }
	    }
        }


	stage('-Build App'){
		agent any
	 	environment {
        		AACCESS_TOKEN = credentials('6ef6ab6d-4f21-46d1-a173-e97f829e294c')
    		}

		steps {
			git(
        		        url:  'git@github.com:mkpmanish/djangoapp.git',
             			   branch: 'dev',
               			 changelog: true,
               			credentialsId: '6ef6ab6d-4f21-46d1-a173-e97f829e294c',
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
                
		
		environment{
			ACCESS_TOKEN=credentials('6ef6ab6d-4f21-46d1-a173-e97f829e294c');
		}
		 steps { 
		:
		  script{
                    try{
			sh 'cat ./checkstatus.sh'
                        echo "Runing Checks if High is present or not..........."
                        sh 'chmod +x checkstatus.sh && ./checkstatus.sh'
			echo "${env.ACCESS_TOKEN}"
			echo "$ACCESS_TOKEN"
			sh "printenv"
                   } catch(Exception e){
                        echo "Bandit Scan failed for some reason...." + e.getMessage()
                }
	     }
           }
        }


	stage('Post-Merge Actions') {
                environment{
                        ACCESS_TOKEN=credentials('6ef6ab6d-4f21-46d1-a173-e97f829e294c');
                }

            steps {
                script {try{
			echo "$ACCESS_TOKEN"
				echo "Inside Post-Merge"
				echo 'running post merge and commenting'
                                sh 'chmod +x post_comment.sh'
                                sh "./post_comment.sh $ACCESS_TOKEN"
				//echo 'date=$(date) && curl -X POST -H "Authorization: token $ACCESS_TOKEN"   -d \'{ "body": "successfull - $date" }\'  \'https://api.github.com/repos/mkpmanish/djangoapp/issues/40/comments\''
                  }catch(Exception e){
			echo "exception"
		  }
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
