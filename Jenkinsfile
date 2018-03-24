#!groovy
// This deployment script assumes that there is only a single Jenkins server (master) and there are no agents.
// If the setup includes agents, then the stages should be reconfigured to take advantage of additional remote nodes.
// This script is assuming that you're using a multi-branch project but the majority directly translates to a regular pipeline project.
def notifySlack(String buildStatus = 'SUCCESS') {
    def color
    def msg

    if (buildStatus == 'SUCCESS') {
        color = '#BDFFC3'
        msg = "${buildStatus}: `${env.JOB_NAME}` #${env.BUILD_NUMBER}"
    } else {
        color = '#FF9FA1'
        msg = "${buildStatus}: `${env.JOB_NAME}` #${env.BUILD_NUMBER}:\n${env.BUILD_URL}"
    }

    slackSend(color: color, message: msg)
}

node {
    
    try {
        // It's often recommended to run a django project from a virtual environment.
        // This way you can manage all of your depedencies without affecting the rest of your system.
        def venvTestExists = fileExists '/home/ubuntu/prehab-tests/bin/activate'
        def venvProdExists = fileExists '/home/ubuntu/prehab/bin/activate'

        if (!venvProdExists) {
            stage("Install Python Virtual Enviroment for Production") {
                sh 'cd /home/ubuntu/prehab'
                sh 'sudo virtualenv --no-site-packages .'
            }
        } 
        if (!venvTestExists) {
            stage("Install Python Virtual Enviroment for Tests") {
                currentBuild.stage = 
                sh 'cd /home/ubuntu/prehab-tests'
                sh 'sudo virtualenv --no-site-packages .'
            }
        } 
        
        // Unit Tests made in a different folder
        stage ("Unit Tests") {
            sh '''
                cd /home/ubuntu/prehab-tests
                sudo git pull origin master
                # source /home/ubuntu/prehab-tests/bin/activate
                sudo pip3 install -r requirements.txt
               #deactivate
                sudo python3 manage.py test
            '''
        }
        
        // If tests are ok
        stage ("Deployment") {
            sh '''
                cd /home/ubuntu/prehab/
                sudo git pull origin master
                sudo screen -S prehab_backend -d -m python3 manage.py runserver 0.0.0.0:8000
                sudo pkill screen
                sudo screen -S prehab_backend -d -m python3 manage.py runserver 0.0.0.0:80
            '''
        }
        
        currentBuild.result = 'SUCCESS'
    } catch (e) {
        // Notify Error 
        currentBuild.result = 'FAILURE'
        throw e
    } finally {
        // notify Success
        notifySlack(currentBuild.result)
    }
}
