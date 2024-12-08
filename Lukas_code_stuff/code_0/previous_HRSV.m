%% resolution for Assignment 3 Human responce Exp4 to S&V
% @chenya
% 02/2023
clear
close all
%load file
filepath=('/Users/elliot/Documents/CTHAppliedAcoustic/HRSV23_Assignment3/matlab');
da=load(fullfile(filepath,'HRSV_Home_assignment_2023_part_3.mat'));

%% 1 mean and confidence interval
expNo=fieldnames(da.experiment_4_data);
for i=2:size(expNo,1)
    tempmean=mean(da.experiment_4_data.(expNo{i}),1);  
    errobar=confiInt(da.experiment_4_data.(expNo{i}),1);  
    %results.mean=cat(1,results.mean,tempmean);
    outResults.("mconf"+num2str(i-1))=cat(1,tempmean,(tempmean-errobar),(tempmean+errobar));
    clear tempmean
    clear errobar
end
labeldim=i-1;
clear i;

% Create generic labels
P_labels{1}="Annoyance";
P_labels{2}="Tonality";
P_labels{3}="Sharpness";
P_labels{4}="Loudness";
P_labels{5}="Powerfulness";

resultnames = fieldnames(outResults); 
for nr = 1 : size(resultnames,1)
  tempresult.(resultnames{nr}) = outResults.(resultnames{nr})';
  savename = "exp_4_"+P_labels{nr}+"_stat.mat";
  save(savename,'-struct', 'tempresult');
  clear tempresult savename
end

%% 2 spider plot
% need to fix the scale of the plot

%data
P=zeros(5,5,13);
for j=1:13
    for i=1:labeldim
        P(1:3,i,j)=cat(2,outResults.("mconf"+num2str(i))(:,j));
    end
    P(4,:,j)=[9 9 9 9 9];
    P(5,:,j)=[1 1 1 1 1];
end
clear j

% for ii = 1:num_of_points
%     P_labels{ii} = sprintf('Label %i', ii);
% end

%tiledlayout(4,4);


for z=1:13
    nexttile
    % Figure properties
    %figure('units', 'normalized', 'outerposition', [0 0.05 1 0.95]);
    
    % Axes properties
    axes_interval = 4;
    axes_precision = 1;
    
    % Spider plot
    spider_plot(P(:,:,z), P_labels, axes_interval, axes_precision,...
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


%% 3 correlation over dimension
cormatrix=zeros(5,5); %correlation matrix 
for i=1:5
    for j=1:5
        tempcor=corrcoef(outResults.("mconf"+num2str(i))(1,:),outResults.("mconf"+num2str(j))(1,:));
        cormatrix(i,j)=tempcor(1,2);
%         cormatrix(j,j)=tempcor(2,1);
        clear tempcor;
    end
end
clear i
clear j

save(' exp_4_corr.mat',"cormatrix");
%% 4 artimes
calda=load('exp_4_psycho_par.mat').exp_4_psycho_par;

%% 5 corralation over calculation and perceiption
cormatrix2=zeros(8,1);
perceptionA=outResults.("mconf"+num2str(1));
for i=1:8
    temp=corrcoef(calda(:,i),perceptionA(1,:));
    cormatrix2(i,1)=temp(2,1);
    clear temp;
end
clear i;

save("exp_4_corr_pp.mat","cormatrix2");
%% 6 perdiction
% 1 4 6
x1=calda(:,1);
x2=calda(:,4);
x3=calda(:,6);
X=[ones(size(x1)) x1 x2 x3];
y=perceptionA(1,:)';
[b,~,~,~,status]= regress(y,X);
pa=b(1)+b(2)*x1+b(3)*x2+b(4)*x3;
%pa=perdiction(calda,perceptionA(1,:)');

save("exp_4_pa.mat","pa");
%% ex plot
%tbl = readtable('patients.xls');
scatter3(x1,x2,x3,40,y,'filled');
%s.SizeData = 100;
colorbar
%isosurface
%% 7 plot
figure('Name','perdiction')
%scatter([1 2 3 4 5 6 7 8 9 10 11 12 13],perceptionA,'filled');
set(gcf, 'Color', [1, 1, 1]); % white figure background
set(gcf, 'Position', [00 00 1000 2*300]); % figure size and aspect ratio
errorbar(perceptionA(1,:),(perceptionA(1,:)-perceptionA(2,:)), "o", "MarkerSize", 10, "LineWidth",1.75)
box on;
hold on
scatter([1 2 3 4 5 6 7 8 9 10 11 12 13],pa,'red','filled');
hold off
grid on
ylim([0,9])
% xlim([0.3,8.7])
xlabel('Stimuli' , 'interpreter', 'latex', 'Fontsize', 18);
ylabel('Annoyance' , 'interpreter', 'latex', 'Fontsize', 18);
legend({'Perception','Perdiction'},'location', 'bestoutside','FontSize',18 )

thickenall_big
%% 8 the coefficient of determination R2 and the root mean squared error 𝜀

% mdl=fitlm(X,y);
% RSq=mdl.Rsquared.Ordinary;
epsilon=rmse(pa',perceptionA(1,:));
RSq=status(1);
resultQ8=cat(1,RSq,epsilon);
save("exp_4_corr_rmse_pa.mat","resultQ8");
%% 9 cross validation analysis
%X is the dataset
%choose how many sets
p = 11;
%// List all combinations choosing 3 out of 1:8.
fullset=repmat(1:13,78,1);
newset = nchoosek(1:size(calda,1), p);
%vNewset=setdiff(fullset',newset','rows'); 
%// Use each row of v to create the matrices, and put the results in an cell array.
%// This is the A matrix in your question.
newCalda = arrayfun(@(k)calda(newset(k,:), :), 1:size(newset,1), 'UniformOutput', false);
%vNewCalda = arrayfun(@(k)calda(vNewset(k,:), :), 1:size(vNewset,1), 'UniformOutput', false);
%newCalda is a cell.use newCalda{1,n} to get the combination
newPerceptionA=arrayfun(@(k)perceptionA(1,newset(k,:)), 1:size(newset,1), 'UniformOutput', false);
%vNewPerceptionA=arrayfun(@(k)perceptionA(1,vNewset(k,:)), 1:size(vNewset,1), 'UniformOutput', false);
newpa=zeros(1,78);
newRSq=zeros(1,78);
newandvNewError=zeros(78,1);
bb=zeros(4,78);
for i=1:78
   [bb(:,i),newRSq(i),error]=perdiction(newCalda{1,i},newPerceptionA{1,i});

   vNewset=setdiff(fullset(i,:),newset(i,:)); 
   vNewCalda=calda(vNewset, :);
   vNewPerceptionA=perceptionA(1,vNewset);
   x1=vNewCalda(:,1);
   x2=vNewCalda(:,4);
   x3=vNewCalda(:,6);

   % according to b calculated above 
   vNewPa=bb(1,i)+bb(2,i)*x1+bb(3,i)*x2+bb(4,i)*x3;

   newandvNewError(i,1)=error;
   newandvNewError(i,2)=rmse(vNewPa,vNewPerceptionA');

end
clear i

% plot
figure('name','R^2');
boxplot(newRSq);
xlabel('All combinations');
ylabel('Coefficient of Determine');
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',16,'FontWeight','normal')
set(gca,'XTickLabelMode','auto');

figure('name','RMS Error');
boxplot(newandvNewError);
ylabel('Root mean square error');
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',16,'FontWeight','normal')
set(gca,'XTickLabelMode','auto')
xticks([1 2])
xticklabels({'training data','validation data'});



figure('name','Beta');
tiledlayout(2,2);
edge=-8:0.5:0;
% Tile 1
nexttile
histogram(bb(1,:));
title('\beta_{0}','FontSize',16);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',16,'FontWeight','normal')
set(gca,'XTickLabelMode','auto')
% Tile 2
nexttile
histogram(bb(2,:));
ylim([0,40]);
title('\beta_{1}','FontSize',16);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',16,'FontWeight','normal')
set(gca,'XTickLabelMode','auto')
% Tile 3
nexttile
histogram(bb(3,:));
title('\beta_{2}','FontSize',16);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',16,'FontWeight','normal')
set(gca,'XTickLabelMode','auto')
% Tile 4
nexttile
histogram(bb(4,:));
title('\beta_{3}','FontSize',16);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',16,'FontWeight','normal')
set(gca,'XTickLabelMode','auto')



% figure('Name','histogram');
% [newpa,newRSq,newepsilon]=perdiction(newCalda,perceptionA(1,1:11));
% hold on
% [vNewpa,vNewRSq,vNewepsilon]=perdiction(vNewCalda,perceptionA(1,11:13));
% hold off
% xlabel('value of beta');
% ylabel('number of values');
% legend('first 11 sets','validation data');



%% 
function data_err  = confiInt(data,dim)
    p = 0.05; % confidence interval 95%
    %DIM = 3; % dimension, change if necessary
    data_std = std(data, 0, dim); % standard deviation
    data_sem = data_std/sqrt(length(data));
    data_ts = tinv(1-p/2, length(data)-1);
    data_err = data_ts * data_sem;
end
%%
function [b,RSq,epsilon,pa]=perdiction(calda,perceptionAmean)
    x1=calda(:,1);
    x2=calda(:,4);
    x3=calda(:,6);
    X=[ones(size(x1)) x1 x2 x3];
    y=perceptionAmean';
   [b,~,~,~,status]= regress(y,X);
    RSq=status(1);
    pa=b(1)+b(2)*x1+b(3)*x2+b(4)*x3;
    epsilon=rmse(pa,y);
    %edge=-10:2:10;
    %histogram(b,edge);
end
%%
% for i=2:size(expNo,1)
%     if i==2
%     results.mean=mean(da.experiment_4_data.(expNo{i}),1);  
%     errobar=confiInt(da.experiment_4_data.(expNo{i}),1);  
%     
% %     results.Uppconfi=(results.mean+errobar);  
% %     results.Lowconfi=results.mean-errobar;  
%     outResults.("mconf"+num2str(i))=cat(1,results.mean',(results.mean-errobar)',(results.mean+errobar)');
%     else
%     tempmean=mean(da.experiment_4_data.(expNo{i}),1);  
%     errobar=confiInt(da.experiment_4_data.(expNo{i}),1);  
%     results.mean=cat(1,results.mean,tempmean);
% %     
% %     results.Uppconfi=cat(1,results.Uppconfi,(tempmean+errobar));  
% %     results.Lowconfi=cat(1,results.Lowconfi,(tempmean-errobar)); 
% 
%     outResults.("mconf"+num2str(i))=cat(1,tempmean',(tempmean-errobar)',(tempmean+errobar)');
%     clear tempmean
%     end
% end


% %% n choose k example
% X = [2,6,1; 3,8,1; 4,7,1; 6,2,1; 6,4,1; 7,3,1; 8,5,1; 7,6,1];
% p = 3;
% %// List all combinations choosing 3 out of 1:8.
% v = nchoosek(1:size(X,1), p);
% %// Use each row of v to create the matrices, and put the results in an cell array.
% %// This is the A matrix in your question.
% A = arrayfun(@(k)X(v(k,:), :), 1:size(v,1), 'UniformOutput', false);
% %// And you can concatenate A vertically to get c.
% flatA = cellfun(@(x)reshape(x, 1, []), A, 'UniformOutput', false);
% c = vertcat(flatA{:});