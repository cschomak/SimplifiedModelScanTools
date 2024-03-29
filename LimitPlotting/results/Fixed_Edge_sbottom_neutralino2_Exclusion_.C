{
//=========Macro generated from canvas: c_squ/c_squ
//=========  (Tue Nov  4 13:43:39 2014) by ROOT version5.34/07
   TCanvas *c_squ = new TCanvas("c_squ", "c_squ",1,1,900,776);
   gStyle->SetOptStat(0);
   c_squ->SetHighLightColor(2);
   c_squ->Range(69.08783,-30.40541,761.6554,797.2973);
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
   
   TH2F *92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV] = new TH2F("92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]","",41,193.75,706.25,49,93.75,706.25);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->SetStats(0);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->SetLineStyle(0);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetXaxis()->SetTitle("m(#tilde{b}) [GeV]");
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetXaxis()->SetNdivisions(505);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetXaxis()->SetLabelFont(42);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetXaxis()->SetLabelOffset(0.007);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetXaxis()->SetTitleSize(32);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetXaxis()->SetTitleFont(43);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetYaxis()->SetTitle("m(#tilde{#chi}_{2}^{0}) [GeV]");
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetYaxis()->SetLabelFont(42);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetYaxis()->SetLabelOffset(0.007);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetYaxis()->SetTitleSize(32);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetYaxis()->SetTitleOffset(1.5);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetYaxis()->SetTitleFont(43);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetZaxis()->SetLabelFont(42);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetZaxis()->SetLabelOffset(0.007);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetZaxis()->SetTitleSize(32);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetZaxis()->SetTitleOffset(1.2);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->GetZaxis()->SetTitleFont(43);
   92487219_m(#tilde{b}) [GeV]_m(#tilde{#chi}_{2}^{0}) [GeV]->Draw("h");
   
   TGraph *graph = new TGraph(23);
   graph->SetName("Observed limit");
   graph->SetTitle("Observed limit");
   graph->SetFillColor(100);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#0000ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);
   graph->SetPoint(0,343.75,100);
   graph->SetPoint(1,343.75,112.5);
   graph->SetPoint(2,343.75,125);
   graph->SetPoint(3,343.75,137.5);
   graph->SetPoint(4,343.6045,149.8544999);
   graph->SetPoint(5,342.7837813,161.5337812);
   graph->SetPoint(6,340.5482846,171.7982846);
   graph->SetPoint(7,336.5337813,180.2837812);
   graph->SetPoint(8,331.1045,187.3545);
   graph->SetPoint(9,325,193.75);
   graph->SetPoint(10,318.75,200);
   graph->SetPoint(11,312.3545,206.1045);
   graph->SetPoint(12,305.2837812,211.5337813);
   graph->SetPoint(13,296.7982846,215.5482846);
   graph->SetPoint(14,286.5337812,217.7837813);
   graph->SetPoint(15,274.8544999,218.6045);
   graph->SetPoint(16,262.5,218.75);
   graph->SetPoint(17,250.1197198,218.6045);
   graph->SetPoint(18,238.3465809,217.8095615);
   graph->SetPoint(19,227.8055396,215.8392028);
   graph->SetPoint(20,219.1515959,212.8960939);
   graph->SetPoint(21,210.9088591,210.0175204);
   graph->SetPoint(22,200,208.2979194);
   
   TH1F *Graph_Graph1 = new TH1F("Graph_Graph1","Observed limit",100,185.625,358.125);
   Graph_Graph1->SetMinimum(88.125);
   Graph_Graph1->SetMaximum(230.625);
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
   
   graph = new TGraph(44);
   graph->SetName("Expected limit");
   graph->SetTitle("Expected limit");
   graph->SetFillColor(100);

   ci = TColor::GetColor("#cc3300");
   graph->SetLineColor(ci);
   graph->SetLineStyle(9);
   graph->SetLineWidth(3);
   graph->SetPoint(0,431.3955001,100);
   graph->SetPoint(1,432.2162188,111.8472832);
   graph->SetPoint(2,434.3062154,122.0892847);
   graph->SetPoint(3,437.3545,131.1044999);
   graph->SetPoint(4,439.7275659,139.5899966);
   graph->SetPoint(5,439.7275659,147.9100034);
   graph->SetPoint(6,437.3545,156.3955001);
   graph->SetPoint(7,434.3062154,165.5562153);
   graph->SetPoint(8,432.0707187,175.8207187);
   graph->SetPoint(9,430.4292813,186.6792813);
   graph->SetPoint(10,428.1937847,196.9437847);
   graph->SetPoint(11,425,206.25);
   graph->SetPoint(12,421.6607153,215.4107153);
   graph->SetPoint(13,418.75,225);
   graph->SetPoint(14,415.6937847,234.4437847);
   graph->SetPoint(15,411.3882812,242.6382812);
   graph->SetPoint(16,405.2837812,249.0337812);
   graph->SetPoint(17,397.7645034,254.0145034);
   graph->SetPoint(18,389.7354966,258.4854967);
   graph->SetPoint(19,382.0707187,263.3207187);
   graph->SetPoint(20,375,268.75);
   graph->SetPoint(21,367.9292813,274.1792813);
   graph->SetPoint(22,360.2645034,279.0145034);
   graph->SetPoint(23,352.2354966,283.1944965);
   graph->SetPoint(24,344.5707187,286.3882812);
   graph->SetPoint(25,337.5,287.6375693);
   graph->SetPoint(26,330.2837812,286.5337813);
   graph->SetPoint(27,321.7982846,284.1864956);
   graph->SetPoint(28,311.5337812,282.3616369);
   graph->SetPoint(29,299.9742197,281.6203136);
   graph->SetPoint(30,288.4663008,280.7041682);
   graph->SetPoint(31,278.6521205,277.8192331);
   graph->SetPoint(32,271.2403284,272.4595163);
   graph->SetPoint(33,265.2476175,265.9264469);
   graph->SetPoint(34,259.0735531,259.7523825);
   graph->SetPoint(35,252.3949836,253.930952);
   graph->SetPoint(36,246.069048,247.6050164);
   graph->SetPoint(37,240.2476175,240.9264469);
   graph->SetPoint(38,234.0735531,234.7523825);
   graph->SetPoint(39,227.3949836,228.930952);
   graph->SetPoint(40,221.069048,222.6050164);
   graph->SetPoint(41,216.0159851,216.0977273);
   graph->SetPoint(42,210.192052,211.0095194);
   graph->SetPoint(43,200,208.4434195);
   
   TH1F *Graph_Graph2 = new TH1F("Graph_Graph2","Expected limit",100,176.0272,463.7003);
   Graph_Graph2->SetMinimum(81.23624);
   Graph_Graph2->SetMaximum(306.4013);
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
