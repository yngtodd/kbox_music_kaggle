"""
Data preprocessing.
"""
import pandas as pd


def preprocess(input_path="/Users/youngtodd/data/kaggle/kbox_music/"):
    """
    """
    test = pd.read_csv(input_path + 'test.csv', dtype={'msno': 'category',
                                                       'source_system_tab': 'category',
                                                       'source_screen_name': 'category',
                                                       'source_type': 'category',
                                                       'song_id': 'category'})

    train = pd.read_csv(input_path + 'train.csv', dtype={'msno': 'category',
                                                         'source_system_tab': 'category',
                                                         'source_screen_name': 'category',
                                                         'source_type': 'category',
                                                         'target': np.uint8,
                                                         'song_id': 'category'})

    members = pd.read_csv(input_path + 'members.csv', dtype={'city': 'category',
                                                             'bd': np.uint8,
                                                             'gender': 'category',
                                                             'registered_via': 'category'},
                                                             parse_dates=['registration_init_time','expiration_date'])

    songs = pd.read_csv(input_path + 'songs.csv', dtype={'genre_ids': 'category',
                                                            'language': 'category',
                                                            'artist_name': 'category',
                                                            'composer': 'category',
                                                            'lyricist': 'category',
                                                            'song_id': 'category'})

    # Convert date to number of days
    members['membership_days'] = (members['expiration_date'] - members['registration_init_time']).dt.days.astype(int)

    # Remove both date fieldsa since we already have the number of days between them
    members = members.drop(['registration_init_time','expiration_date'], axis=1)

    # Merge the members dataframe into the test dataframe
    test = pd.merge(left = test,right = df_members,how='left',on='msno')
    test.msno = test.msno.astype('category')

    # Merge the member dataframe into the train dataframe
    train = pd.merge(left = train,right = df_members,how='left',on='msno')
    train.msno = train.msno.astype('category')

    # Release memory
    del members

    # Merge the Test Dataframe with the SONGS dataframe
    test = pd.merge(left = test,right = songs,how = 'left',on='song_id')
    test.song_length.fillna(200000,inplace=True)
    test.song_length = test.song_length.astype(np.uint32)
    test.song_id = test.song_id.astype('category')

    # Merge the Train dataframe with the SONGS dataframe
    train = pd.merge(left = train,right = songs,how = 'left',on='song_id')
    train.song_length.fillna(200000,inplace=True)
    train.song_length = train.song_length.astype(np.uint32)
    train.song_id = train.song_id.astype('category')

    # Release memory
    del songs
    return train, test
