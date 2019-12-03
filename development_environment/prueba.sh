docker run -v $PWD/../app/:/tmp/code webpp/codestyle -i /tmp/code -x '/tmp/code/docs' '/tmp/code/migrations'
    if [ $? -lt 1 ]
        then
            echo "\n##############################################################\n"
            echo "Codestyle errors fixed.\n"
            echo "##############################################################\n"
        else
            echo "\n###########################################################################\n"
            echo "There are unfixables code-style errors, run make code-style-verbose to see the errors.\n"
            echo "###########################################################################\n"
            exit 1
            
    fi