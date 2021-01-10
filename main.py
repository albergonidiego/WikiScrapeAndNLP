import OpenSearch
import tools
import wikiScraper
import engineNLP
import datetime
import PySimpleGUI as sg


def main():

    # Set the stage
    global wiki_dict
    global wiki_content
    global searched_strings

    wiki_dict = {}
    wiki_content = {}
    searched_strings = []
    sg.theme('DefaultNoMoreNagging')
    placeholder = ['Wikipedia articles will appear here', '']
    placeholder2 = 'Scraped content will appear here'
    placeholder3 = 'NLP summary will appear here'
    placeholderLoading = ['... loading ...', '']
    spacing = ""
    # Create filler for bottom buttons
    for i in range(136):
        spacing += " "
    risposta = None

    # Define window content
    layout = [[sg.Text("What would you like to search? ", key='_title_')],
              [sg.InputText(key='_input_', size=(85,1)), sg.Button('SEARCH', size=(12, 1), bind_return_key=True)],
              [sg.Text("Search results")],
              [sg.Listbox(values=placeholder, text_color='black', key='_results_', size=(83, 5)),
               sg.B("SCRAPE &\nSUMMARISE", key='_run_', size=(12, 5))
               ],
              [sg.Multiline(placeholder2, text_color='black', size=(100, 15), key='_scrape_')],
              [sg.Multiline(placeholder3, text_color='blue', size=(100, 10), key='_summary_')],
              [sg.B("SAVE RESULTS"), sg.Text(spacing), sg.B("QUIT")]
              ]
    # Create window
    window = sg.Window("Wiki Search & Summarise", layout)

    # GUI
    while True:
        event, values = window.read()

        # Handle GUI events
        if event in (None, sg.WINDOW_CLOSED, 'QUIT'):
            # If the dictionary is not empty save it
            if bool(wiki_content):
                tools.salva_dict(wiki_content, 'wiki_articles_viewed')
            if searched_strings is not None:
                tools.salva_dict(searched_strings, 'searched_strings')
            window.close()
            break

        # Call the wikipedia openSearch API using as search query the value inputed by the user
        if event == "SEARCH":
            try:
                ricerca = values['_input_']
                datetime_now = datetime.datetime.now()
                datetime_now_usable = datetime_now.strftime("%Y%m%d%H%M%S")
                temp = [datetime_now_usable, ricerca]
                searched_strings.append(temp)
                print(searched_strings)
                if ricerca == "":
                    sg.Popup('Please input a search value', keep_on_top=True)
                else:
                    # Show loading message in the relevant box
                    show_results(placeholderLoading, window)
                    # Search for Wikipedia articles matching the search string
                    risposta = OpenSearch.wiki_search(ricerca)
                    print(risposta[1])
                    # Create dictionary of articles -> URLs
                    wiki_dict = dict(zip(risposta[1],risposta[3]))
                    print(wiki_dict)
                    show_results(risposta[1], window)
            except Exception as ex:
                print(ex)

        # Start the Scraping of the selected Wikipedia web page
        if event == "_run_":
            try:
                whatToScrape = values['_results_']
                if not whatToScrape:
                    sg.Popup('You must search and select a Wikipedia article first', keep_on_top=True)
                elif len(whatToScrape) > 1:
                    print("Only one item can be selected")
                    break
                else:
                    datetime_now = datetime.datetime.now()
                    datetime_now_usable = datetime_now.strftime("%Y%m%d%H%M%S")
                    show_scrape('_scrape_', '... loading ...', window)
                    show_scrape('_summary_', '... AI engine in motion, please wait. This may take up to 1 minute ...', window)
                    strWhatToScrape = ""
                    for item in whatToScrape:
                        strWhatToScrape += item

                    URLtoScrape = wiki_dict[strWhatToScrape]

                    testo, titolo = wikiScraper.scrape_Wiki(URLtoScrape)
                    show_scrape('_scrape_', testo, window)
                    summary = engineNLP.nlp_it(testo, 150)
                    print(summary)
                    show_scrape('_summary_', summary, window)
                    wiki_content[datetime_now_usable] = {
                        'timestamp': datetime_now_usable,
                        'URL': URLtoScrape,
                        'title': titolo,
                        'text': testo,
                        'ai_summary': summary
                    }
                    # wiki_content.update({
                    #     'timestamp': datetime_now_usable,
                    #     'URL': URLtoScrape,
                    #     'title': titolo,
                    #     'text': testo,
                    #     'ai_summary': summary
                    #     }
                    # )

            except Exception as ex:
                print(ex)
                break

        # Save the Wiki openSearch response as text, includes case handling and dialog to get the filename from user
        if event == "SAVE":
            if risposta is None:
                sg.Popup('Please search first', keep_on_top=True)
            else:
                layoutSave = [[sg.Text("Save search results")],
                          [sg.Text("What would you like the file to be called?  ", key='_title_')],
                          [sg.InputText(key='_inputSave_'), sg.Button('SAVE')],
                          [sg.B("QUIT")]
                          ]
                windowSave = sg.Window("Save search results", layoutSave)
                while True:
                    eventSave, valuesSave = windowSave.read()
                    if eventSave in (None, sg.WINDOW_CLOSED, 'QUIT'):
                        windowSave.close()
                        break
                    if eventSave == "SAVE":
                        try:
                            filename = valuesSave['_inputSave_']
                            if filename == "":
                                sg.Popup('Please input a filename', keep_on_top=True)

                            else:
                                fileSaved = tools.salva_json(risposta, filename)
                                sg.Popup(fileSaved + ' saved.', keep_on_top=True)
                                windowSave.close()
                                break
                        except Exception as ex:
                            print(ex)
                            break

# Function to update the listbox items using the article title passed by Wikipedia
def show_results(risposta, window):
    window['_results_'].update(values=risposta)
    # newString = ""
    # for item in risposta:
    #     newString += item + '\n'
    # print(newString)
    # window['_results_'].update(newString)
    window.Refresh()

def show_scrape(elemento, testo, window):
    window[elemento].update(testo)
    window.Refresh()

######################################################################################################################

if __name__ == "__main__":
    main()