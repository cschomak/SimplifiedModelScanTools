{
//=========Macro generated from canvas: c_squ/c_squ
//=========  (Wed Jun  4 14:09:25 2014) by ROOT version5.32/00
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
   
   TH2F *284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV] = new TH2F("284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]","",26,190,710,31,90,710);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->SetStats(0);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->SetLineStyle(0);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetTitle("M_{sbottom} [GeV]");
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetNdivisions(505);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetLabelFont(42);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetLabelOffset(0.007);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetTitleSize(32);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetXaxis()->SetTitleFont(43);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitle("M_{neutralino 2} [GeV]");
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetLabelFont(42);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetLabelOffset(0.007);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitleSize(32);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitleOffset(1.5);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetYaxis()->SetTitleFont(43);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetLabelFont(42);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetLabelOffset(0.007);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetTitleSize(32);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetTitleOffset(1.2);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->GetZaxis()->SetTitleFont(43);
   284060386_M_{sbottom} [GeV]_M_{neutralino 2} [GeV]->Draw("h");
   
   TGraph *graph = new TGraph(11);
   graph->SetName("Observed limit");
   graph->SetTitle("Observed limit");
   graph->SetFillColor(100);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#0000ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   graph->SetPoint(0,290,100);
   graph->SetPoint(1,289.7671999,119.7671999);
   graph->SetPoint(2,288.2212499,138.2212499);
   graph->SetPoint(3,283.5641055,153.5641054);
   graph->SetPoint(4,274.8772554,164.8772554);
   graph->SetPoint(5,263.3439945,172.8783943);
   graph->SetPoint(6,251.3131499,178.2212499);
   graph->SetPoint(7,240,180.2201109);
   graph->SetPoint(8,229.4983968,178.45405);
   graph->SetPoint(9,217.3602594,174.6571445);
   graph->SetPoint(10,200,171.7787502);
   
   TH1F *Graph_Graph3 = new TH1F("Graph_Graph3","Observed limit",100,191,299);
   Graph_Graph3->SetMinimum(91.97799);
   Graph_Graph3->SetMaximum(188.2421);
   Graph_Graph3->SetDirectory(0);
   Graph_Graph3->SetStats(0);
   Graph_Graph3->SetLineStyle(0);
   Graph_Graph3->GetXaxis()->SetNdivisions(505);
   Graph_Graph3->GetXaxis()->SetLabelFont(42);
   Graph_Graph3->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3->GetXaxis()->SetTitleSize(32);
   Graph_Graph3->GetXaxis()->SetTitleFont(43);
   Graph_Graph3->GetYaxis()->SetLabelFont(42);
   Graph_Graph3->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3->GetYaxis()->SetTitleSize(32);
   Graph_Graph3->GetYaxis()->SetTitleOffset(1.5);
   Graph_Graph3->GetYaxis()->SetTitleFont(43);
   Graph_Graph3->GetZaxis()->SetLabelFont(42);
   Graph_Graph3->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3->GetZaxis()->SetTitleSize(32);
   Graph_Graph3->GetZaxis()->SetTitleOffset(1.2);
   Graph_Graph3->GetZaxis()->SetTitleFont(43);
   graph->SetHistogram(Graph_Graph3);
   
   graph->Draw("l");
   
   graph = new TGraph(18);
   graph->SetName("Expected limit");
   graph->SetTitle("Expected limit");
   graph->SetFillColor(100);

   ci = TColor::GetColor("#cc3300");
   graph->SetLineColor(ci);
   graph->SetLineStyle(9);
   graph->SetLineWidth(3);
   graph->SetPoint(0,351.7787502,100);
   graph->SetPoint(1,354.8899446,117.5930595);
   graph->SetPoint(2,360,131.0443468);
   graph->SetPoint(3,364.8772554,144.6571444);
   graph->SetPoint(4,366.9081,160);
   graph->SetPoint(5,364.6444553,175.1100555);
   graph->SetPoint(6,358.45405,188.45405);
   graph->SetPoint(7,349.7671999,199.7671999);
   graph->SetPoint(8,339.7671999,209.7671999);
   graph->SetPoint(9,328.45405,218.45405);
   graph->SetPoint(10,314.8772554,224.8772554);
   graph->SetPoint(11,298.45405,228.45405);
   graph->SetPoint(12,279.7671999,229.8084484);
   graph->SetPoint(13,260.1915517,229.9586205);
   graph->SetPoint(14,241.3545295,228.8963796);
   graph->SetPoint(15,224.2012774,225.8470623);
   graph->SetPoint(16,210.0229059,221.0348314);
   graph->SetPoint(17,200,216.9697038);
   
   TH1F *Graph_Graph4 = new TH1F("Graph_Graph4","Expected limit",100,183.3092,383.5989);
   Graph_Graph4->SetMinimum(87.00414);
   Graph_Graph4->SetMaximum(242.9545);
   Graph_Graph4->SetDirectory(0);
   Graph_Graph4->SetStats(0);
   Graph_Graph4->SetLineStyle(0);
   Graph_Graph4->GetXaxis()->SetNdivisions(505);
   Graph_Graph4->GetXaxis()->SetLabelFont(42);
   Graph_Graph4->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph4->GetXaxis()->SetTitleSize(32);
   Graph_Graph4->GetXaxis()->SetTitleFont(43);
   Graph_Graph4->GetYaxis()->SetLabelFont(42);
   Graph_Graph4->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph4->GetYaxis()->SetTitleSize(32);
   Graph_Graph4->GetYaxis()->SetTitleOffset(1.5);
   Graph_Graph4->GetYaxis()->SetTitleFont(43);
   Graph_Graph4->GetZaxis()->SetLabelFont(42);
   Graph_Graph4->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph4->GetZaxis()->SetTitleSize(32);
   Graph_Graph4->GetZaxis()->SetTitleOffset(1.2);
   Graph_Graph4->GetZaxis()->SetTitleFont(43);
   graph->SetHistogram(Graph_Graph4);
   
   graph->Draw("l");
   c_squ->Modified();
   c_squ->cd();
   c_squ->SetSelected(c_squ);
}
