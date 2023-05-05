
%% read data
T = readtable('Survey.csv');

%% cate
personNo=table2array(T(:,3)); %row,column
personMBTI=table2array(T(:,5));

%table2array

personChara={personNo,personMBTI,};