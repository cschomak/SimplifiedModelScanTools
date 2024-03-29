{
//=========Macro generated from canvas: c_squ/c_squ
//=========  (Wed Jun  4 11:16:29 2014) by ROOT version5.32/00
   TCanvas *c_squ = new TCanvas("c_squ", "c_squ",1,1,900,776);
   gStyle->SetOptStat(0);
   c_squ->SetHighLightColor(2);
   c_squ->Range(63.51351,-35.67568,766.2162,802.1622);
   c_squ->SetFillColor(0);
   c_squ->SetBorderMode(0);
   c_squ->SetBorderSize(2);
   c_squ->SetTickx(1);
   c_squ->SetTicky(1);
   c_squ->SetLeftMargin(0.18);
   c_squ->SetRightMargin(0.08);
   c_squ->SetBottomMargin(0.15);
   c_squ->SetFrameFillColor(1);
   c_squ->SetFrameFillStyle(0);
   c_squ->SetFrameLineStyle(0);
   c_squ->SetFrameBorderMode(0);
   
   TH2F *484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV] = new TH2F("484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]","",26,190,710,31,90,710);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->SetStats(0);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->SetLineStyle(0);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetTitle("M_{sbottom} [GeV]");
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetNdivisions(505);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetLabelFont(42);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetLabelOffset(0.007);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetTitleSize(32);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetTitleFont(43);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitle("M_{neutralino 2} [GeV]");
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetLabelFont(42);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetLabelOffset(0.007);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitleSize(32);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitleOffset(1.5);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitleFont(43);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetLabelFont(42);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetLabelOffset(0.007);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetTitleSize(32);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetTitleOffset(1.2);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetTitleFont(43);
   484096098_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->Draw("h");
   
   TGraph *graph = new TGraph(17);
   graph->SetName("Observed limit");
   graph->SetTitle("Observed limit");
   graph->SetFillColor(100);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#0000ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   graph->SetPoint(0,370,100);
   graph->SetPoint(1,370,120);
   graph->SetPoint(2,370,140);
   graph->SetPoint(3,369.7671999,159.7671999);
   graph->SetPoint(4,368.45405,178.45405);
   graph->SetPoint(5,364.8772554,194.8772554);
   graph->SetPoint(6,358.2212499,208.2212499);
   graph->SetPoint(7,348.2212499,218.2212499);
   graph->SetPoint(8,334.8772554,224.8772554);
   graph->SetPoint(9,318.45405,228.45405);
   graph->SetPoint(10,299.7671999,229.7671999);
   graph->SetPoint(11,280,230.0412485);
   graph->SetPoint(12,260.1915517,229.9586205);
   graph->SetPoint(13,241.3545295,228.8963796);
   graph->SetPoint(14,224.2012774,225.8470623);
   graph->SetPoint(15,210.0229059,221.0348314);
   graph->SetPoint(16,200,216.9697038);
   
   TH1F *Graph_Graph1 = new TH1F("Graph_Graph1","Observed limit",100,183,387);
   Graph_Graph1->SetMinimum(86.99588);
   Graph_Graph1->SetMaximum(243.0454);
   Graph_Graph1->SetDirectory(0);
   Graph_Graph1->SetStats(0);
   Graph_Graph1->SetLineStyle(0);
   Graph_Graph1->GetXaxis()->SetNdivisions(505);
   Graph_Graph1->GetXaxis()->SetLabelFont(42);
   Graph_Graph1->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph1->GetXaxis()->SetTitleSize(32);
   Graph_Graph1->GetXaxis()->SetTitleFont(43);
   Graph_Graph1->GetYaxis()->SetLabelFont(42);
   Graph_Graph1->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph1->GetYaxis()->SetTitleSize(32);
   Graph_Graph1->GetYaxis()->SetTitleOffset(1.5);
   Graph_Graph1->GetYaxis()->SetTitleFont(43);
   Graph_Graph1->GetZaxis()->SetLabelFont(42);
   Graph_Graph1->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph1->GetZaxis()->SetTitleSize(32);
   Graph_Graph1->GetZaxis()->SetTitleOffset(1.2);
   Graph_Graph1->GetZaxis()->SetTitleFont(43);
   graph->SetHistogram(Graph_Graph1);
   
   graph->Draw("l");
   
   graph = new TGraph(26);
   graph->SetName("Expected limit");
   graph->SetTitle("Expected limit");
   graph->SetFillColor(100);

   ci = TColor::GetColor("#cc3300");
   graph->SetLineColor(ci);
   graph->SetLineStyle(9);
   graph->SetLineWidth(3);
   graph->SetPoint(0,430,100);
   graph->SetPoint(1,430,120);
   graph->SetPoint(2,430,140);
   graph->SetPoint(3,430,160);
   graph->SetPoint(4,429.7671999,179.7671999);
   graph->SetPoint(5,428.45405,198.45405);
   graph->SetPoint(6,425.1100555,215.1100555);
   graph->SetPoint(7,419.7671999,229.7671999);
   graph->SetPoint(8,413.1111944,243.1111944);
   graph->SetPoint(9,405.1100555,255.1100555);
   graph->SetPoint(10,395.1100555,265.1100555);
   graph->SetPoint(11,383.1111944,273.1111944);
   graph->SetPoint(12,369.7671999,279.7671999);
   graph->SetPoint(13,355.3428556,284.8772554);
   graph->SetPoint(14,340,286.9081);
   graph->SetPoint(15,324.6571444,284.8772554);
   graph->SetPoint(16,310,280.0412484);
   graph->SetPoint(17,295.3016071,274.848565);
   graph->SetPoint(18,279.8085795,270.4423297);
   graph->SetPoint(19,264.4476149,265.8058139);
   graph->SetPoint(20,250.8501916,259.2974608);
   graph->SetPoint(21,239.3893892,250.6543789);
   graph->SetPoint(22,229.112821,240.8846593);
   graph->SetPoint(23,218.9102516,231.1612275);
   graph->SetPoint(24,208.8760145,222.6220298);
   graph->SetPoint(25,200,217.2025039);
   
   TH1F *Graph_Graph2 = new TH1F("Graph_Graph2","Expected limit",100,177,453);
   Graph_Graph2->SetMinimum(81.30919);
   Graph_Graph2->SetMaximum(305.5989);
   Graph_Graph2->SetDirectory(0);
   Graph_Graph2->SetStats(0);
   Graph_Graph2->SetLineStyle(0);
   Graph_Graph2->GetXaxis()->SetNdivisions(505);
   Graph_Graph2->GetXaxis()->SetLabelFont(42);
   Graph_Graph2->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph2->GetXaxis()->SetTitleSize(32);
   Graph_Graph2->GetXaxis()->SetTitleFont(43);
   Graph_Graph2->GetYaxis()->SetLabelFont(42);
   Graph_Graph2->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph2->GetYaxis()->SetTitleSize(32);
   Graph_Graph2->GetYaxis()->SetTitleOffset(1.5);
   Graph_Graph2->GetYaxis()->SetTitleFont(43);
   Graph_Graph2->GetZaxis()->SetLabelFont(42);
   Graph_Graph2->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph2->GetZaxis()->SetTitleSize(32);
   Graph_Graph2->GetZaxis()->SetTitleOffset(1.2);
   Graph_Graph2->GetZaxis()->SetTitleFont(43);
   graph->SetHistogram(Graph_Graph2);
   
   graph->Draw("l");
   c_squ->Modified();
   c_squ->cd();
   c_squ->SetSelected(c_squ);
}
