// --------------------------------------------------------------------------
// Licensed Materials - Property of IBM
//
// 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55
// Copyright IBM Corporation 1998, 2022. All Rights Reserved.
//
// Note to U.S. Government Users Restricted Rights:
// Use, duplication or disclosure restricted by GSA ADP Schedule
// Contract with IBM Corp.
// --------------------------------------------------------------------------

/*******************************************************************************
OPL Model for Air Traffic Flow Management

これは航空交通管理の問題である。重要な航空区画の混雑を避けるため、飛行機の離陸が遅れる。

エアキャパシティの制限は、規制期間、つまり1時間ごとの容量率を持つ区画で表現される。
規制航空交通区画には、1つまたは複数の規制期間がある。
フライトには予想離陸時間（ETOT）があり、これは時間、分、秒で指定され、合計分数に変換される。
An enter event specifies that a given flight will enter a given sector at an expected time (called expected time over).

The objective is to minimize the total sum of flight delays.

*******************************************************************************/
using CP;

int nbOfFlights = ...;
range Flights = 1 .. nbOfFlights;

{string} SectorNames = ...;

// 時刻は時間、分、秒で指定される
// (一般的には、年、月、日も同様)
tuple Time {
   int hours;
   int minutes;
   int seconds;
};

// 1時間あたりの容量率. capacity rate はこの値で決まる
tuple Period {
   Time start;
   Time end;
   int rate;
};
{Period} periods[SectorNames] = ...;

// 進入イベント. どのフライトが、どの区画に、どの時刻で（expected time over?）来るか
tuple Enter {
   int flight;
   string sector;
   Time eto;
};

int nbOfEnters = ...;
range Enters = 1 .. nbOfEnters;
Enter e[Enters] = ...;

// フライトが遅れていいのは2時間まで
int maxDelay = 120;

// 10分のタイムスタンプで区切る
int timeStep = 10;

// 以下、最適化モデル
// フライトごとの遅延分数. 整数で表す
dvar int delay[Flights] in 0 .. maxDelay;

// 各進入イベントは持続時間1, つまり10分かかるものとする
dvar interval a[Enters] size 1;

// 各区画はリソースとして扱う. interval 変数 a が各区画において何個来ているか?
cumulFunction r[i in SectorNames] = sum(en in Enters : e[en].sector == i) pulse(a[en], 1);

// CPLEX の設定. FailLimit とは?
execute {
  		cp.param.FailLimit = 20000;
}

dexpr int totalDelay = sum(i in Flights) delay[i];
minimize totalDelay;

constraints {

  // 容量率は10分間隔に修正される
  // ex: 7:30-8:00 で rate 30 だった場合, interval変数 a によって各フライトの進入開始時刻が決まるので,
  // pulse(a[en], 1) により 7:30-8:00 に進入するイベント数がわかる.
  // そこから割合が30%以内になるようにする?
  forall (i in SectorNames)
      forall (p in periods[i])
         alwaysIn(r[i], (p.start.hours * 60 + p.start.minutes) div timeStep,
                        (p.end.hours * 60 + p.end.minutes) div timeStep,
                           0,
                        (p.rate * timeStep + 59) div 60);


   // フライトは、予想されるタイムオーバーに遅延を加えた時間でセクターに入る;
   // リソースの時間スケールはタイムステップで割られるため、アクティビティ開始時刻も同じようにする
   forall (i in Enters)
      startOf(a[i]) == (delay[e[i].flight] + e[i].eto.hours * 60 + e[i].eto.minutes) div timeStep;

   forall(i in SectorNames)
     r[i] <= nbOfFlights;
}

execute {
  writeln("total delay = " + totalDelay);
}
