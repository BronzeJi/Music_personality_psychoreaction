%clear outResults
clear
close all
%% 0 Loading data
%load("importeddata.mat");
T= readtable('data/da_59.xlsx','Format','auto');
currentFolder = pwd;
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

%% 1
%expNo=fieldnames(da.experiment_4_data);
genreName = fieldnames(person.song);

for i=1:(size(genreName,1)-1)
    tempmean=mean(person.song.(genreName{i}),1);  
    errobar=confiInt(person.song.(genreName{i}),1);  
    %results.mean=cat(1,results.mean,tempmean);
    outResults.("song"+num2str(i))=cat(1,tempmean,(tempmean-errobar),(tempmean+errobar),zeros(1,9),ones(1,9)*5);
    clear tempmean
    clear errobar
end
labeldim=i;
clear i;

% Create generic labels
P_labels{1}="Happy";
P_labels{2}="Sad";
P_labels{3}="Energetic";
P_labels{4}="Agressive";
P_labels{5}="Calm";
P_labels{6}="Annoyed";
P_labels{7}="Pleased";
P_labels{8}="Like";
P_labels{9}="Emotional";
%P_labels{10}="Know";

%% 2 spider plot
% need to fix the scale of the plot


% for ii = 1:num_of_points
%     P_labels{ii} = sprintf('Label %i', ii);
% end

%tiledlayout(4,4);


for z=1:12  % 12 songs 
    nexttile
    % Figure properties
    %figure('units', 'normalized', 'outerposition', [0 0.05 1 0.95]);
    
    % Axes properties
    axes_interval = 4;
    axes_precision = 1;
    
    % Spider plot
    spider_plot(outResults.("song"+num2str(z)), P_labels, axes_interval, axes_precision,...
        'Marker', 'o',...
        'LineStyle', '-',...
        'LineWidth', 2,...
        'MarkerSize', 10);
    
    % Title properties
    title(("Set "+num2str(z)),...
        'Fontweight', 'bold',...
        'FontSize', 24);
    
    % Legend properties
   
    %saveas(gcf,fullfile(filepath,("Spider_Set_"+num2str(z)+".png")));
end
 legend('Arithmetic Mean','Lower CI','Upper CI','Location', 'best','FontSize', 12);
    hold off
clear z
saveas(gcf,fullfile(currentFolder,'/figure/spider.png'));

%% 2 Correlation
%data
P=zeros(10,12); %12 songs
for j=1:12
    for i=1:9 %9 label
        P(i,j)=cat(2,outResults.("song"+num2str(j))(1,i));
    end
end
clear j

cormatrix=zeros(9,9); %correlation matrix 
for i=1:9
    for j=1:9
        tempcor=corrcoef(P(i,:),P(j,:));
        cormatrix(i,j)=tempcor(1,2);
%         cormatrix(j,j)=tempcor(2,1);
        clear tempcor;
    end
end
clear i
%%
figure(2);
heatmap(P_labels,P_labels,cormatrix);
saveas(gcf,fullfile(currentFolder,'figure/Cor_sur.png'));
%%





%% 
function data_err  = confiInt(data,dim)
    p = 0.05; % confidence interval 95%
    %DIM = 3; % dimension, change if necessary
    data_std = std(data, 0, dim); % standard deviation
    data_sem = data_std/sqrt(length(data));
    data_ts = tinv(1-p/2, length(data)-1);
    data_err = data_ts * data_sem;
end