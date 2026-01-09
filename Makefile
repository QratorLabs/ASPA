NAME1=draft-ietf-sidrops-aspa-verification
NAME2=draft-ietf-sidrops-aspa-profile

.PHONY: all
all: drafts

.PHONY: drafts
drafts: $(NAME1).txt $(NAME2).txt

$(NAME1).txt: $(NAME1).xml
	xml2rfc $(NAME1).xml --html --text --expand --allow-local-file-access

$(NAME2).txt: $(NAME2).xml
	xml2rfc $(NAME2).xml --html --text --expand --allow-local-file-access

clean:
	rm -f $(NAME1)*.html $(NAME2)*.html $(NAME1)*.txt $(NAME2)*.txt
