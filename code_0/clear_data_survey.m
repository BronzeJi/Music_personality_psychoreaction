
%% read data
T = readtable('da.csv');
n=10;


%% clear data

%% category
person.No=table2array(T(:,3)); %row,column
person.MBTI=table2array(T(:,5));

for z=9:9:133 %the first question of one song
    tempmusicOnesong=zeros(1,n);
    for j=z:z+9 %the first question of one song
        Musicpref= table2array(T(:,j));
        %regexp("4(test",'\d*','Match');%get the number%table2array
        c=regexp(Musicpref,'\d*','Match');%get the number
        tempmusic=str2num(cell2mat(c{1}));
            for i=2:n
                temp=str2num(cell2mat(c{i}));
                tempmusic=[tempmusic,temp];
            end
        tempmusicOnesong=cat(2,tempmusicOnesong,tempmusic); 
         clear c tempmusic temp 
        %tempmusiccel
        
    end
        tempmusiccell=num2cell(tempmusicOnesong(2:10,:)');
        person.Musicpref{1,j-8}=tempmusiccell; % score per music per feeling
        clear tempmusicOnesong tempmusiccell
end

%% draft
% n=133;
% temp=[];
% c=regexp(person.Musicpref,'\d*','Match');%get the number
% for i=1:n
%     temp=[temp catcell2mat(c{i})];
% end
% person.Musicpref{1}=tempcell;