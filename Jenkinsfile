pipeline {
    agent none
   credentials {
        usernamePassword(credentialsId: '6ef6ab6d-4f21-46d1-a173-e97f829e294c', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')
    }
    stages {
	stage('-Build App'){
		agent any
		steps {
			git(
        		        url:  'git@github.com:mkpmanish/djangoapp.git',
             			   branch: 'main',
               			 changelog: true,
               			 poll: true
                	)
			sh 'grep -ri 8888 *'
			sh 'uname -a'
			sh 'hostname'
			sh 'docker build -t myhellopy .'
			sh 'docker run -p 8800:8800 -d myhellopy'
			sh 'sleep 10'
			sh 'curl http://$(curl http://checkip.amazonaws.com):8800/'
		  		
		}
	}


        stage("Run SAST - Bandit"){
                agent any
                steps { script{
                   try{
                        echo "Runing SCA scan..........."
                        sh 'docker run --rm --volume /var/lib/jenkins/workspace/NS-GITHUB-JENKINS:/src:rw secfigo/bandit:latest > output.txt'
                	sh 'cat output.txt'
		} catch(Exception e){
                        echo "Bandit Scan failed for some reason...." + e.getMessage()
                }}
           }
        }

	stage("Check Bandit & Comment"){
                agent any
                steps { scripts {
                        try{
				echo "Runing Checks..........."
                        	sh 'chmod +x checkstatus.sh && ./checkstatus.sh'
                        	//sh """curl -X POST -H 'Accept: application/json' https://api.github.com/repos/mkpmanish/djangoapp/dispatches -d '{ \"ref\": \"\$(git rev-parse --abbrev-ref HEAD)\", \"event_type\": \"pull_request\" }' -u $GIT_USERNAME:$GIT_PASSWORD"""
                                sh "curl -X POST -H 'Authorization: token ' ${GIT_USERNAME}:${GIT_PASSWORD} ' https://api.github.com/repos/mkpmanish/djangoapp/pulls/\$(github pullRequest number)/reviews -d '{ \"body\": \"Successful build! Automatically approved.\", \"event\": \"APPROVE\" }'"
			} catch(Exception e){
				echo "Build failed! Skipping merge."	
				sh "curl -X POST -H 'Accept: application/json' https://api.github.com/repos/your-org/your-repo/dispatches \
                        -d '{ \"ref\": \"$(git rev-parse --abbrev-ref HEAD)\", \"event_type\": \"pull_request\" }' \
                        -u $GIT_USERNAME:$GIT_PASSWORD"
				sh "git config core.commentSignOff false && git commit --empty --message 'Build failed. Merge blocked.' && git push origin HEAD:main"i
				sh "git status"
				echo "Ending Checks -------------"	
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
