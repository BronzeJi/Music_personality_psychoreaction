%% Deleting text from strings

function out = textRemover(genre) 
for i = 1:size(genre,1)
    for j = 1:size(genre,2)
        if contains(genre(i,j),'0')
            genre(i,j) = 0;
        elseif contains(genre(i,j),'1')
            genre(i,j) = 1;
        elseif contains(genre(i,j),'2')
            genre(i,j) = 2;
        elseif contains(genre(i,j),'3')
            genre(i,j) = 3;
        elseif contains(genre(i,j),'4')
            genre(i,j) = 4;
        elseif contains(genre(i,j),'5')
            genre(i,j) = 5;
        end
    end
end
genre(1:1,:) = [];

out = str2double(genre);

end