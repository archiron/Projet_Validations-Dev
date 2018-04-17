from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()

from ROOT import *
from fonctions import getHisto

from DataFormats.FWLite import Handle, Events
from optparse import Values
options = Values()
options.secondaryInputFiles = argv[2:] 
options.maxEvents = -1

eleStyle = ROOT.gStyle
eleStyle.SetCanvasBorderMode(0)
eleStyle.SetCanvasColor(kWhite)
eleStyle.SetCanvasDefH(600)
eleStyle.SetCanvasDefW(1600)
eleStyle.SetCanvasDefX(0)
eleStyle.SetCanvasDefY(0)
eleStyle.SetPadBorderMode(0)
eleStyle.SetPadColor(kWhite)
eleStyle.SetPadGridX(False)
eleStyle.SetPadGridY(False)
eleStyle.SetPadTickX(1)
eleStyle.SetPadTickY(1)
eleStyle.SetPadBottomMargin(0.05)
eleStyle.SetPadTopMargin(0.075)
eleStyle.SetPadLeftMargin(0.15)
eleStyle.SetPadRightMargin(0.2) 
eleStyle.SetGridColor(0)
eleStyle.SetGridStyle(3)
eleStyle.SetGridWidth(1)
eleStyle.SetOptStat(1)
eleStyle.SetHistLineColor(1)
eleStyle.SetHistLineStyle(0)
eleStyle.SetHistLineWidth(2)
eleStyle.SetEndErrorSize(2)
eleStyle.SetErrorX(0.)
eleStyle.SetTitleColor(1, "XYZ")
eleStyle.SetTitleFont(42, "XYZ")
eleStyle.SetTitleXOffset(1.0)
eleStyle.SetTitleYOffset(1.0)
eleStyle.SetTitleSize(0.05, "XYZ")
eleStyle.SetTitleFont(22,"X")
eleStyle.SetTitleFont(22,"Y")
eleStyle.SetTitleStyle(1001)
eleStyle.SetTitleBorderSize(2)
eleStyle.SetLabelOffset(0.005, "XYZ") # numeric label
eleStyle.SetMarkerStyle(2)
eleStyle.SetMarkerSize(0.8)
eleStyle.cd()
gROOT.ForceStyle()

def RenderHisto(histo, canvas):
    if ("ELE_LOGY" in histo.GetOption() and histo.GetMaximum() > 0):
        canvas.SetLogy(1)
    histo_name_flag = 1 ; # use 0 to switch off
    if ( histo.InheritsFrom("TH2") ):
        eleStyle.SetPalette(1)
        eleStyle.SetOptStat(110+histo_name_flag)
    elif ( histo.InheritsFrom("TProfile") ):
        eleStyle.SetOptStat(110+histo_name_flag)
    else: # TH1
        eleStyle.SetOptStat(111110+histo_name_flag)

def PictureChoice(histo1, histo2, fileName):
    if(histo1.InheritsFrom("TH1F")):
#        print "TH1F : 2 pads"
        createPicture(histo_1, histo_2, "GIF/" + histo_name + ".gif")
    else:
#        print "no TH1F, 1 pad"   
        createPicture_2(histo_1, histo_2, "GIF/" + histo_name + ".gif")
        
def createPicture(histo1, histo2, fileName):
    canvas_name = "c" + histo_name
    c = ROOT.TCanvas("canvas0", canvas_name, 0, 0, 960, 900)
    
    pad1 = ROOT.TPad("pad1","pad1",0.05,0.32,0.95,0.95,0,0,0)
    pad2 = ROOT.TPad("pad2","pad2",0.05,0.05,0.95,0.27,0,0,0)
    pad1.Draw("P")
    pad2.Draw("P")

    pad1.cd()
    histo2.Draw()
    histo2.SetStats(1)
    RenderHisto(histo2, c)
    ROOT.gPad.Update()   
    statBox2 = histo2.GetListOfFunctions().FindObject("stats")
    histo2.SetLineColor(kBlue)       #blue
    histo2.SetMarkerColor(kBlue) 
    histo2.SetLineWidth(3) 
    statBox2.SetTextColor(kBlue)

    RenderHisto(histo1, c)
    if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
        pad1.SetLogy(1)
    ROOT.gPad.Update()
    histo1.Draw()
    histo1.SetStats(1)
    c.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    histo1.SetLineColor(kRed)       #red
    histo1.SetMarkerColor(kRed) ;
    statBox1.SetTextColor(kRed)

    if histo2.GetMaximum() > histo1.GetMaximum():
        histo1.SetMaximum(histo2.GetMaximum()*1.1)
    
    y1 = statBox2.GetY1NDC()
    y2 = statBox2.GetY2NDC()
    statBox2.SetY1NDC(2*y1-y2) 
    statBox2.SetY2NDC(y1) 
    
    histo1.Draw()
    histo2.SetLineWidth(3) 
    histo2.Draw("histsames")
    
    pad2.cd()
    histo3 = histo1.Clone()
    histo4 = histo2.Clone()
    histo3.Sumw2()
    histo3.SetStats(0)
    histo3.Divide(histo4)
    histo3.SetTitle("") # remove title
    histo3.Draw("ep")
    histo3.SetMaximum(-1111); #-1111 is a special value to reset the max/min
    histo3.SetMinimum(-1111);

    c.Update()
    Hist_File_Name = fileName # dossier + 
    c.Print (Hist_File_Name)
    c.Closed()

def createPicture_2(histo1, histo2, fileName):
    canvas_name = "c" + histo_name
    canvas = ROOT.TCanvas("canvas0", canvas_name, 0, 0, 960, 660)
    pad = ROOT.TPad("pad","pad",0.05,0.05,0.95,0.95,0,0,0)
    pad.Draw("P")
    
    pad.cd()
    histo2.Draw()
    histo2.SetStats(1)
    RenderHisto(histo2, canvas)
    ROOT.gPad.Update()
    statBox2 = histo2.GetListOfFunctions().FindObject("stats")
    histo2.SetLineColor(kBlue)       #blue
    histo2.SetMarkerColor(kBlue) 
    histo2.SetLineWidth(3) 
    statBox2.SetTextColor(kBlue)

    RenderHisto(histo1, canvas)
    ROOT.gPad.Update()
    histo1.Draw()
    histo1.SetStats(1)
    canvas.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    histo1.SetLineColor(kRed)       #red
    histo1.SetMarkerColor(kRed) ;
    statBox1.SetTextColor(kRed)

    if histo2.GetMaximum() > histo1.GetMaximum():
        histo1.SetMaximum(histo2.GetMaximum()*1.1)
    
    y1 = statBox2.GetY1NDC()
    y2 = statBox2.GetY2NDC()
    statBox2.SetY1NDC(2*y1-y2) 
    statBox2.SetY2NDC(y1) 
    
    histo1.Draw()
    histo2.SetLineWidth(3) 
    histo2.Draw("histsames")
    canvas.Update()

    Hist_File_Name = fileName # dossier + 
    canvas.Print (Hist_File_Name)
    canvas.Closed()

input_rel_file = "8_1_0_pre12/DQM_V0001_R000000001__RelValTTbar_13__CMSSW_8_1_0_pre12-81X_mcRun2_asymptotic_v8-v1__DQMIO.root"
input_ref_file = "8_1_0_pre12/8_1_0_pre11/DQM_V0001_R000000001__RelValTTbar_13__CMSSW_8_1_0_pre11-81X_mcRun2_asymptotic_Candidate_2016_08_30_11_31_55-v1__DQMIO.root"

f_rel = ROOT.TFile(input_rel_file)
f_rel.ls()
h1 = getHisto(f_rel)

f_ref = ROOT.TFile(input_ref_file)
f_ref.ls()
h2 = getHisto(f_ref)

CMP_CONFIG = 'ElectronMcSignalHistos.txt'
f = open(CMP_CONFIG, 'r')
wp = open('index.html', 'w') # web page
wp.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
wp.write("<html>\n")
wp.write("<head>\n")
wp.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
wp.write("<title> CMP_TITLE </title>\n") #option -t dans OvalFile
wp.write("</head>\n")
wp.write("<a NAME=\"TOP\"></a>")
wp.write("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"../../../../img/up.gif\" alt=\"Up\"/></a>&nbsp; CMP_TITLE </h1>\n" ) # option -t dans OvalFile

if (f_ref==0):
    wp.write("<p>In all plots below, there was no reference histograms to compare with")
    wp.write(", and the CMP_RED_FILE histograms are in red.") # new release red in OvalFile
else:
    wp.write("<p>In all plots below")
    wp.write(", the <b><font color='red'> CMP_RED_FILE </font></b> histograms are in red") # new release red in OvalFile
    wp.write(", and the <b><font color='blue'> CMP_BLUE_FILE </font></b> histograms are in blue.") # ref release blue in OvalFile

#wp.write(" " + "red_comment" + " " + "blue_comment" + " Some more details") # comments form OvalFile. No more used
wp.write(": <a href=\"electronCompare.C\">script</a> used to make the plots")
wp.write(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms") # .txt file
wp.write(", <a href=\"gifs/\">images</a> of histograms" + "." ) # 
wp.write("</p>\n")

wp.write("<br><table border=\"1\" cellpadding=\"5\" width=\"100%\"><tr valign=\"top\">")
#read lines
counter = 0
blanck = False
cat_num = -1
for line in f:
    line_read = line.split()
    if ( len(line_read) == 0 ):
        if ( blanck == False ):
            counter += 1
            blanck = True
    else: # nb != 0
        if (counter == 1): # Title
            wp.write("<td width=\"20%\">\n")
            blanck = False
            cat_num += 1
            wp.write("<b>" + line + "</b><br><br>\n")
        else: # general case, histos
            counter = 0
            blanck = False
            histo_name = (line_read[0].split("/"))[1]
            short_histo_name = histo_name.replace("h_","")
            if ("ele_" in short_histo_name):
                short_histo_name = short_histo_name[4:]
            if ("_barrel" in short_histo_name):
                wp.write("<a href=\"#" + short_histo_name + "\">" + "barrel" + "</a>")
            elif ("_endcaps" in short_histo_name):
                wp.write("<a href=\"#" + short_histo_name + "\">" + "endcaps" + "</a>")
            else:
                wp.write("<a href=\"#" + short_histo_name + "\">" + short_histo_name + "</a>") # + " " + str(line_read[3]) + ":" + str(line_read[4]) 
            wp.write("&nbsp;\n" )
            if ( line_read[3]=="1" or line_read[4]=="1" ):
                wp.write("<br>\n")
            if ( line_read[4]=="1" ): # end of group
                wp.write("<br></td>\n")
                if (cat_num==4):
                    wp.write("</tr>\n<tr valign=\"top\">" )
                    cat_num = -1

wp.write("<br></td></tr></table>\n")

f.seek(0) # rewind file
counter = 0
wp.write("\n\n<br><br><table cellpadding=\"5\">\n")
for line in f:
    line_sp = line.split()
    nb = len(line_sp)
    if (nb == 0):
        counter += 1
        wp.write("<tr valign=\"top\">")
        wp.write("\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=\"img/up.gif\" alt=\"Top\"/></a></td>\n<td>")
    else: # nb != 0
        if (counter == 1): # Title
            print "\n", line 
            wp.write("\n<br><br><b>" + line + "</b><br>")
            wp.write("</td></tr>\n")
        else: # general case, histos
            counter = 0
            histo_name = (line_sp[0].split("/"))[1]
            short_histo_name = histo_name.replace("h_","")
            gif_name = "GIF/" + histo_name + ".gif" # GIF to be rename into gifs
            if ("ele_" in short_histo_name):
                short_histo_name = short_histo_name[4:]
            histo_1 = h1.Get(histo_name)
            histo_2 = h2.Get(histo_name)
            PictureChoice(histo_1, histo_2, "GIF/" + histo_name + ".gif")
            if ( line_sp[3]=="0" ):
                wp.write("<a id=\"" + histo_name + "\" name=\"" + short_histo_name + "\"></a>")
                wp.write("<a href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a><br>")
                wp.write("</td>\n<td>")
            else: # line_sp[3]=="1"
                wp.write("<a id=\"" + histo_name + "\" name=\"" + short_histo_name + "\"></a>")
                wp.write("<a href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a><br>")
                wp.write("</td>\n</tr>")
                if ( line_sp[4]=="0" ):
                    wp.write("<tr valign=\"top\">")
                    wp.write("\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=\"img/up.gif\" alt=\"Top\"/></a></td>\n<td>")

wp.write("</td></tr></table>\n")
wp.write("\n</html>")
f.close()
wp.close()
    
# picture with histos only
canvas_name = "c" + "h_recTrackNum" # c + histoname
canvas = ROOT.TCanvas("canvas1", canvas_name, 0, 0, 600, 600) 
h_recTrackNum_1 = h1.Get("h_recTrackNum")
h_recTrackNum_2 = h2.Get("h_recTrackNum")
h_ele_Et_1 = h1.Get("h_ele_Et")
h_ele_Et_2 = h2.Get("h_ele_Et")
h_ele_photonRelativeIso_1 = h1.Get("h_ele_photonRelativeIso")
h_ele_photonRelativeIso_2 = h2.Get("h_ele_photonRelativeIso")
createPicture(h_recTrackNum_1, h_recTrackNum_2, "h_recTrackNum.jpg")
createPicture(h_ele_photonRelativeIso_1, h_ele_photonRelativeIso_2, "h_ele_photonRelativeIso.jpg")
canvas.Closed()

# picture with histos and histos division
canvas_name2 = "c" + "h_ele_Et" # c + histoname
canvas2 = ROOT.TCanvas("canvas2", canvas_name2, 0, 0, 600, 800) 
canvas2.Divide(1,2)

pad3 = ROOT.TPad("pad1","pad1",0,0.3,1,1,0,0,0)
pad3.SetTopMargin(0.2)
pad3.Draw()
pad3.cd()
h_recTrackNum_2.Draw()
statBox2 = h_recTrackNum_2.GetListOfFunctions().FindObject("stats")
h_recTrackNum_1.Draw("histsames")

canvas2.cd()
pad4 = ROOT.TPad("pad2","pad2",0,0,1,0.3,0,0,0)
pad4.SetTopMargin(0)
pad4.Draw()
pad4.cd()
h_ele_Et_3 = h_ele_Et_1.Clone()
h_ele_Et_4 = h_ele_Et_2.Clone()
h_ele_Et_3.Sumw2()
h_ele_Et_3.SetStats(0)
h_ele_Et_3.Divide(h_ele_Et_4)
h_ele_Et_3.SetTitle("Bin by Bin Ratio of h1 and h2")

h_ele_Et_3.Draw("ep")
canvas2.Update()
canvas2.Print ("h_ele_Et.jpg")
canvas2.Closed()

print "Fin."
