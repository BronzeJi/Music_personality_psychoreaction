%clear outResults
%clear
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
P_labels{8}="Like songs?";
P_labels{9}="Emotional";
%P_labels{10}="Know song?";

%% 2 spider plot
% need to fix the scale of the plot

%data
% P=zeros(5,5,12); %12 songs
% for j=1:12
%     for i=1:labeldim
%         P(1:3,i,j)=cat(2,outResults.("song"+num2str(i))(:,j));
%     end
%     P(4,:,j)=[9 9 9 9 9];
%     P(5,:,j)=[1 1 1 1 1];
% end
% clear j

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




%% 
function data_err  = confiInt(data,dim)
    p = 0.05; % confidence interval 95%
    %DIM = 3; % dimension, change if necessary
    data_std = std(data, 0, dim); % standard deviation
    data_sem = data_std/sqrt(length(data));
    data_ts = tinv(1-p/2, length(data)-1);
    data_err = data_ts * data_sem;
end