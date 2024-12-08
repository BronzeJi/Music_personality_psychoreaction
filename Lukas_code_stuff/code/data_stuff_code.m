clear
clc

%% Loading data
%load("importeddata.mat");
T= readtable('da_59.xlsx','Format','auto');
     %       ^^^^^^^^^------ your csv filename
%p=T{:,1};
%q=T{:,2};
%save('importeddata_1.mat','p','q')
  %   ^^^^^^^^^----- your resulting .mat filename   
%Musicengineeringanswers=zeros(2);
Musicengineeringanswers=string(T{:,2});
for i=3:135
    Musicengineeringanswers=cat(2,Musicengineeringanswers,string(T{:,i}));
end
clear i
%Musicengineeringanswers=T(:,2:135);
%% Remove text emotions

person.song.Rock = textRemover(Musicengineeringanswers(:,8:16));

person.song.Metal = textRemover(Musicengineeringanswers(:,17:25));

person.song.Techno = textRemover(Musicengineeringanswers(:,26:34));

person.song.EDM = textRemover(Musicengineeringanswers(:,35:43));

person.song.Hardstyle = textRemover(Musicengineeringanswers(:,44:52));

person.song.Jazz = textRemover(Musicengineeringanswers(:,53:61));

person.song.Classical = textRemover(Musicengineeringanswers(:,62:70));

person.song.Pop = textRemover(Musicengineeringanswers(:,71:79));

person.song.RnB = textRemover(Musicengineeringanswers(:,80:88));

person.song.Film = textRemover(Musicengineeringanswers(:,89:97));

person.song.Kpop = textRemover(Musicengineeringanswers(:,98:106));

person.song.Indie = textRemover(Musicengineeringanswers(:,107:115));

person.song.PlayMusic = yesNo_data_remover(Musicengineeringanswers(:,6));



