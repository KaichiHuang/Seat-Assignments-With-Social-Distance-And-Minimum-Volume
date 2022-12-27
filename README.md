# Seat Assignments With Social Distance and Minimum Volume

## 1.Background

受到covid-19的影響，各國政府紛紛針對公共場合人與人之間須保持社交距離的限制，而根據參考文獻，我們可以利用輸入一個已知的空間layout圖及最小社交距離來求解最大可用座位數，在本研究中我們也另外考慮了在社交距離的限制下，人與人之間仍須具備溝通的能力，也就是最小音量的限制，使得座位安排除了能滿足社交距離外，也能夠讓人們維持正常的談話、溝通，同時也透過許多的方法，如：決定音箱(擴音設備)、防疫隔板設置的位置，達到更多可用座位的目標。以下將介紹如何透過Excel檔輸入座標產生空間layout圖，並使用Python的Gurobi Optimizer求解最大可用座位，再利用Python的Matplotlib繪圖套件產生座位分布圖。
## 2.Methodology

### 2.1使用公式介紹

首先我們需要先設置一個室內空間的座標作為輸入，如下圖，我們使用一間教室作為範例，透過在Excel中輸入教室中的每一個座位之座標來得到layout圖。
![layout](https://user-images.githubusercontent.com/120470999/209468847-e1474e67-8803-4466-b187-4bb308fd4d77.jpg)
接著使用Euclidean distance（歐式距離）公式來計算座位中心與座位中心之間的距離，以下為二維及三維的距離計算公式。

#### 2.1.1二維空間距離計算之公式

![二維空間距離計算之公式](https://user-images.githubusercontent.com/120470999/209348419-3daadda5-54cc-4692-9a1f-50797d4f6694.jpg)

#### 2.1.2三維空間距離計算之公式

![三維空間距離計算之公式](https://user-images.githubusercontent.com/120470999/209348461-95d149fd-8a57-43d1-bca9-4b3631a3db0b.jpg)

在計算完每個座位間的距離後，便可以使用分貝的計算公式來計算音量大小，根據inverse square law（平方反比定律），我們可以發現音量會隨著距離的平方而變小，下列公式假設一般談話的音量在10英寸的範圍內約60分貝，將距離帶入公式後，所得之分貝需大於等於我們設置的最小分貝數。

#### 2.1.3分貝計算公式

![分貝計算公式](https://user-images.githubusercontent.com/120470999/209550358-e8fff1e2-afff-480f-a1fa-f0c343284404.jpg)

### 2.2 情境介紹

在我們的研究中將座位的安排分成兩種情境，分別是個人座位以及群組座位，個人座位指每一個座位都是獨立的，具有齊一性，群組的座位則是組內的座位不受距離限制，組與組之間存在最小社交距離的限制，而在考慮音量限制時，個人座位的部分是指設定一個講者(老師)的座標，由這一個位置對應到所有的位置，群組座位則是同一組內的座位存在最小分貝的限制，能夠聽到彼此的聲音進行溝通，下圖為考慮音量的兩個場景示意圖。

![兩種音量情境示意圖](https://user-images.githubusercontent.com/120470999/209642329-fb17c8dd-7be2-4dc9-bf77-5c7d66700ae1.jpg)


### 2.3 模型設置



## 3.Data Collection and Analysis Result


### 3.1個人座位安排

### 3.2群組座位安排

根據教室座位的原先佈置，經由以下幾種情境，例如只考慮社交距離、加以考慮交談音量、增加隔板的設置等，可根據各種限制與設置的不同，而創建不同的座位安排。首先為輸入的資料，以此樣本為例，教室共100個座位，座位表如附檔，為平面二維座標(x, y)；亦須輸入組別資料，而本專案的組人數為1~5數值隨機生成而來，組別資料如附檔。
以下介紹幾種情境與之結果：

#### 3.2.1 只考慮社交距離

在群組的座位安排中，假設組與組間設有社交距離，組內沒有社交距離限制，座位安排由組別號(GroupID)依序排入座位中。如下圖所示，在組間社交距離為20英吋(約50公分)的限制下，所得結果紅字為各個組別的可用座位，打叉藍字為不可使用的座位，結果會因為教室座位佈置、社交距離限制與組別設置這三個因素而有所不同。結果顯示，此例中在教室內100個座位，可容納16個組別，共44人。

![教室只考慮社交距離的群組結果](https://user-images.githubusercontent.com/117344390/209489873-d31eb297-af27-452e-99da-971a47451ba7.png)

#### 3.2.2 加以考慮交談音量

從3.2.1小節的結果可發現，雖然將小組依序排入座位，但有可能會發生組員被分於教室的兩端(如小組10)，反而使組內難以交談，而失去組別安排座位的目的，為了讓組內組員能夠清楚溝通，加以新增音量限制，人與人正常可交談音量為60分貝，音量會因距離越遠而分貝數越小，因此限制最低可交談音量為45分貝，小於45分貝則不符合座位安排。在組間社交距離20英吋的限制，新增最小音量45分貝限制，在同樣的教室座位佈置與組別設置下，結果顯示可容納14個組別，共42人。如下圖所示，雖然可容納人數減少，相對也讓座位安排更加便利與和諧。

![教室加以考慮交談音量的群組結果](https://user-images.githubusercontent.com/117344390/209495283-48c5e277-8986-4b24-a647-a2a8bbcae55c.png)


#### 3.2.3 增加隔板設置

為減少疫情傳播的機率，生活中常以隔板來達到保護人群的效果，有了隔板就可以考慮減少社交距離，因此在該案例中，除社交距離、音量限制外，我們將社交距離減少至15英吋，並且在組的後一個位置新增隔板，以黑色符號 | 作為隔板，結果由下圖所示，結果顯示可容納22個組別，共66人。此方法不僅可以增加容納人數，亦可在不同的環境中設定合理的限制。

![教室增加隔板設置的群組結果](https://user-images.githubusercontent.com/117344390/209497324-ae4f5883-e7a1-456e-9b3f-686d993ee36b.png)

### 3.3其他應用

#### 3.3.1 演講廳

除二維空間外，我們也考量了三維度的階梯演講廳，為三維座標(x, y, z)座位。
以165個可用座位的演講廳為例，在社交距離為20英吋(約50公分)、音量限制45分貝下，輸入演講廳座位座標及組別資料，結果如下圖所示，可容納21組，共有64個可用座位。

![演講廳加以考慮交談音量的群組結果](https://user-images.githubusercontent.com/117344390/209534603-fa91bfe9-9f1b-4280-9039-756a892d5c85.png)



若是減少社交距離為10英吋，並且增加隔板設置，在相同輸入資料下，結果如下圖所示，可容納40組，共有115個可用座位。此設置大幅提高可用座位。

![演講廳增加隔板設置的群組結果](https://user-images.githubusercontent.com/117344390/209520062-a98cf7a0-90b1-49e0-83ac-aa42a65c6aa1.png)


#### 3.3.2 客機

客機的座位亦可用此模型完成座位安排，機艙座位較教室與演講廳不規則，座位間距離依據座位大小與機艙形狀而不固定，因此在群組情況下，假設設定社交距離20英吋、組人數為隨機1~4人，結果如下圖所示，客機座位設定於二維度座標，在213個可用座位下，可容納32組，共78位乘客。

![客機只考慮社交距離的群組結果](https://user-images.githubusercontent.com/117344390/209521220-061159fe-9402-4f0b-a2d1-3bd8eaffbf04.png)


4.Conclusion
----------
本案例匯入座位與群組資料的Excel檔，透過Python結合Gurobi Optimizer求解最大可用座位，再利用Python的Matplotlib套件繪圖，得到座位安排圖。從以上模型與結果，可知座位安排非常多元，除有個人與群組的座位設置外，更有多種不同的環境設置，以下統整三點該模型的特色與實用性：

●社交距離規定：近年為遵守政府政策並避免傳染風險，我們設計並最大化了社交距離規定下的座位分配模型。

●客製化的限制：該模型可以依據不同的環境與假設自行更改參數，亦可添增其他限制，例如本案例增加最小音量限制、增加隔板設置等

●多樣化的情境：該模型可應用在任何座位佈置下，除本次提到的二維度的教室、三維度的演講廳、客機外，也適合應用於日常生活中的情景，如餐廳。
