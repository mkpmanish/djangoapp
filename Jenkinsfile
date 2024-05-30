pipeline {
    agent none
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

	stage('Merge Pull Request') {
		  // Assuming the SSH credential ID is 'ssh-key-id'
  		git branch: 'origin/main', credentialsId: '721fc518-0dae-4898-949c-c14d67c2c877'

 		 if ( !catchError {
   			sh './checkstatus.sh'
  		}) {
    		error('Build or tests failed. Merge aborted.')
   		 return
  		}
	
 		 // Perform merge using Git commands
		  sh "git merge origin/${ENV_CHANGE_ID}"
		  sh "git push origin master"
	}



	stage("Cleanup"){
		agent any
		steps{
			sh 'if [ $(docker ps | awk \'{print $1}\' | tail -1) ];then docker stop $(docker ps | awk \'{print $1}\' | tail -1);fi'
		}
	}
    }
}
