# Projet_Validations-Dev
New version of CMS Electron Validation GUI

path to the GUI on GitHub : https://github.com/archiron/Projet_Validations-Dev

paths to twiki : https://twiki.cern.ch/twiki/bin/view/Main/ElectronValidationGUIHelpPage
path to Releases on eos : http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/Releases/ [1]
path to Dev on eos : http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/Dev
path to GUI on eos : /eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/Validation-Project-DEV
and use it with : python /eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/Validation-Project-DEV/main.py

[1] : by clicking on a folder you are using the new web page with filters made with PHP. If you want the "classical" view, click on 'classical view'. 

before using it, you need :
cmsrel CMSSW_X_Y_Z[_preT]
cd CMSSW_X_Y_Z[_preT]/src
cmsenv
git cms-addpkg Validation/RecoEgamma and then
cd Validation/RecoEGamma/test

